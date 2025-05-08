# StudyBuddy - Your AI Study Companion

StudyBuddy is an intelligent study companion that helps you learn and understand your course materials through interactive conversations. Upload your study materials (PDFs) and chat with an AI that responds like a friendly peer, breaking down complex concepts and helping you learn more effectively.

##  Features

- **Smart PDF Processing**: Upload your study materials and let StudyBuddy process them for intelligent Q&A
- **Interactive Learning**: Chat with an AI that responds like a friendly study buddy
- **Context-Aware Responses**: Get answers based on the specific content of your study materials
- **Multiple Document Support**: Upload and switch between different study materials
- **Modern, User-Friendly Interface**: Clean and intuitive design for a great learning experience
- **Real-time Processing**: Get instant responses to your questions
- **Drag & Drop Support**: Easy file upload with drag and drop functionality

##  Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Ollama installed and running locally

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/studybuddy.git
cd studybuddy
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Start Ollama and pull the required model:
```bash
ollama pull qwen2.5:3b
```

### Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

##  How to Use

1. **Upload Study Materials**:
   - Click "Choose File" or drag and drop your PDF file
   - Wait for the processing to complete
   - Your study material will appear in the list on the left

2. **Start Learning**:
   - Select a study material from the list
   - Type your question in the chat input
   - Get instant, context-aware responses

3. **Switch Between Materials**:
   - Click on different study materials in the list
   - Chat context will update automatically
   - Clear chat history using the "Clear Chat" button when needed

##  Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **AI Model**: Ollama with Qwen 2.5 3B
- **Embedding Model**: BAAI/bge-m3
- **PDF Processing**: PyMuPDF (fitz)
- 
##  Configuration

The application can be configured by modifying the following parameters in `app.py`:

- `EMBED_MODEL_NAME`: The embedding model to use
- `OLLAMA_MODEL_NAME`: The Ollama model to use
- `TOP_K`: Number of relevant chunks to retrieve
- `CHUNK_SIZE`: Size of text chunks for processing
- `UPLOAD_FOLDER`: Directory for storing uploaded files

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for providing the AI model your work is AMAZIINN

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/yourusername/studybuddy/issues) page
2. Create a new issue if your problem isn't already listed

---

Made with ❤️ for students everywhere and especially my @ENSIASD ones :)
