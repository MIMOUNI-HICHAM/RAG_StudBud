from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import ollama
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime

app = Flask(__name__)


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