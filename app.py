from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import ollama
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime

app = Flask(__name__)

# --- CONFIG ---
EMBED_MODEL_NAME = "BAAI/bge-m3"
OLLAMA_MODEL_NAME = "qwen2.5:3b"
TOP_K = 5
CHUNK_SIZE = 500  # characters
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Global store for multiple PDFs
pdf_store = {}  # {pdf_id: {"filename": str, "chunks": list, "embeddings": np.array, "uploaded_at": datetime}}

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load embed model
embed_model = SentenceTransformer(EMBED_MODEL_NAME)

# Load study buddy prompt
with open('prompt.txt', 'r', encoding='utf-8') as f:
    STUDY_BUDDY_PROMPT = f.read()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_pdf_chunks(pdf_path, chunk_size=CHUNK_SIZE):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def embed_chunks(chunks):
    return embed_model.encode(chunks, convert_to_numpy=True)

def retrieve(query, chunks, chunk_embeddings, top_k=TOP_K):
    query_vec = embed_model.encode(query, convert_to_numpy=True)
    sims = np.dot(chunk_embeddings, query_vec)
    top_indices = sims.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

def chat_with_ollama(query, context):
    full_prompt = f"""{STUDY_BUDDY_PROMPT}

Now, using the following context from the study materials, answer the student's question in a helpful, friendly way:

Context:
{context}

Student's Question:
{query}

Remember to:
1. Be friendly and encouraging
2. Break down complex concepts
3. Use examples when helpful
4. End with a follow-up question
5. Keep the tone light and engaging
"""
    response = ollama.chat(model=OLLAMA_MODEL_NAME, messages=[
        {"role": "user", "content": full_prompt}
    ])
    return response['message']['content']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process PDF
        chunks = read_pdf_chunks(filepath)
        embeddings = embed_chunks(chunks)
        
        # Generate unique ID for this PDF
        pdf_id = str(len(pdf_store) + 1)
        
        # Store in global memory
        pdf_store[pdf_id] = {
            "filename": filename,
            "chunks": chunks,
            "embeddings": embeddings,
            "uploaded_at": datetime.now().isoformat()
        }
        
        return jsonify({
            'message': 'PDF processed successfully',
            'chunks_count': len(chunks),
            'pdf_id': pdf_id,
            'filename': filename
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/pdfs', methods=['GET'])
def list_pdfs():
    pdfs = [
        {
            "id": pdf_id,
            "filename": data["filename"],
            "uploaded_at": data["uploaded_at"]
        }
        for pdf_id, data in pdf_store.items()
    ]
    return jsonify(pdfs)

@app.route('/ask', methods=['POST'])
def ask_question():
    pdf_id = request.json.get('pdf_id')
    if not pdf_id or pdf_id not in pdf_store:
        return jsonify({'error': 'Invalid PDF ID'}), 400
    
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    pdf_data = pdf_store[pdf_id]
    chunks = pdf_data['chunks']
    embeddings = pdf_data['embeddings']
    
    # Get relevant chunks and generate response
    top_chunks = retrieve(question, chunks, embeddings)
    combined_context = "\n\n---\n\n".join(top_chunks)
    answer = chat_with_ollama(question, combined_context)
    
    return jsonify({
        'answer': answer,
        'relevant_chunks': top_chunks
    })

if __name__ == '__main__':
    app.run(debug=True) 