# DocSense_Demo

🚀 **AI-Powered Document Understanding System**

DocSense is an intelligent document processing application that leverages LangGraph, LlamaIndex, and OpenAI to extract, analyze, and visualize information from various document formats.

## Features

- 📄 **Multi-Format Support**: PDF, DOCX, PPTX, Excel, CSV, TXT, and images
- 🤖 **AI Summarization**: Generate concise summaries using GPT-4o-mini
- 🔍 **RAG (Retrieval Augmented Generation)**: Ask questions about your documents
- 📊 **Auto Chart Generation**: Automatically creates visualizations from extracted tables
- 🖼️ **Image Analysis**: Extracts and analyzes images with vision LLM
- 📑 **Table Extraction**: Smart table detection and extraction from PDFs
- 🏷️ **Entity Extraction**: Identifies and extracts named entities

## Architecture

The application uses a **LangGraph state machine** with the following nodes:
- **Loader**: Processes documents and extracts content
- **Indexer**: Builds vector index for RAG
- **Summarizer**: Generates AI summaries
- **RAG**: Answers queries using retrieved context
- **Entity Extractor**: Identifies entities using spaCy
- **Visualizer**: Creates charts and visualizations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/harikrishnancj/DocSense_Demo.git
cd DocSense_Demo
```

2. Create a virtual environment:
```bash
python -m venv env
env\Scripts\activate  # On Windows
# source env/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the backend server:
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

2. Start the Streamlit frontend (in a new terminal):
```bash
streamlit run frontend/app.py
```

3. Open your browser to `http://localhost:8501`

4. Upload a document and choose between:
   - **Summarization**: Get an AI-generated summary
   - **RAG**: Ask questions about the document

## Project Structure

```
DocSense/
├── backend/
│   ├── main.py              # FastAPI server
│   └── app_graph.py         # LangGraph workflow
├── frontend/
│   └── app.py               # Streamlit UI
├── states/
│   ├── doc_state.py         # State schema
│   ├── loader.py            # Document loader
│   ├── indexer.py           # Vector index builder
│   ├── summarizer.py        # AI summarization
│   ├── rag.py               # RAG implementation
│   ├── entities.py          # Entity extraction
│   ├── visualizer.py        # Chart generation
│   └── loaders/             # Format-specific loaders
├── model/
│   └── model.py             # LLM configuration
└── requirements.txt
```

## Technologies Used

- **LangGraph**: Workflow orchestration
- **LlamaIndex**: Document indexing and RAG
- **OpenAI GPT-4o-mini**: Language model
- **FastAPI**: Backend API
- **Streamlit**: Frontend UI
- **Camelot**: PDF table extraction
- **spaCy**: Entity recognition
- **Matplotlib**: Visualization

## License

MIT License

## Author

Created by Harikrishnan CJ
