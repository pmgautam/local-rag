# Local-RAG: A Retrieval-Augmented Generation App Using Local Resources

Local-RAG is a Retrieval-Augmented Generation (RAG) application designed to work entirely with local resources.

## 🚀 Key Components

- **Vector Database**: [Qdrant](https://qdrant.tech/)
- **Language Model**: [Ollama](https://ollama.com/) (Llama 3.1)
- **Embedding Model**: [Snowflake/snowflake-arctic-embed-m-v1.5](https://huggingface.co/Snowflake/snowflake-arctic-embed-m-v1.5)
- **User Interface**: [Streamlit](https://streamlit.io/) 

## Planned Enhancements
1. **Contextual Conversations**
2. **History Tracking using SQlite**
3. **Advanced RAG Features** (reranking, query processing, handling complex queries etc)
4. **Configurable Setup**
5. **Better error handling and logging**

## 🛠️ Installation

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/pmgautam/local-rag.git
   cd local-rag
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Qdrant**
   ```bash
   # Start Qdrant with persistent storage and default ports
   docker run -d \
     -p 6333:6333 \
     -p 6334:6334 \
     -v $(pwd)/qdrant_storage:/qdrant/storage:z \
     qdrant/qdrant
   ```

5. **Install Ollama and download model**
   ```bash
   # Install Ollama from ollama.com
   # Pull the Llama 3.1 model
   ollama pull llama3.1
   ```

## 📚 Usage

### Indexing Documents
```bash
# Index documents with default settings
python -m app.indexer --folder /path/to/documents --collection my_docs
```

### Starting the Application
```bash
# Start with default configuration
streamlit run app/chat_app.py

# Start with custom configuration
streamlit run app/chat_app.py -- --config path/to/config.yaml
```

## 🤝 Contributing

Contributions are welcome! Please send a PR for any improvements you would want to make.
