# Task 2 - RAG AI System

## Project Overview

In this project, I built a RAG (Retrieval-Augmented Generation) AI chatbot using LangChain, ChromaDB, HuggingFace embeddings, Groq API, and Streamlit.

The chatbot can read uploaded PDF files and answer questions based only on the content inside the documents.

---

# Features

* PDF question answering
* Multi-PDF support
* Semantic search
* Chat memory
* Streamlit UI
* Retrieval-based responses
* Display of retrieved chunks

---

# Technologies Used

* Python
* Streamlit
* LangChain
* ChromaDB
* HuggingFace Embeddings
* Groq API

---

# How Retrieval Works

1. The PDF is loaded using `PyPDFLoader`.
2. The document is split into smaller chunks.
3. Embeddings are created for all chunks using the model:
   `all-MiniLM-L6-v2`
4. The chunks and embeddings are stored in ChromaDB.
5. When the user asks a question:

   * similar chunks are retrieved from the database
   * the retrieved chunks are given as context to the Groq model
6. The model generates the final answer using the retrieved context.

---

# Issues Faced

* Retrieved chunks sometimes contained repeated content
* Streamlit reruns caused memory issues initially
* Retrieval sometimes failed for short technical keywords
* API key authentication errors
* Slow loading because embeddings were recreated repeatedly

---

# Folder Structure

```text id="gtq1iw"
Task2/
│
├── app.py
├── rag.py
├── requirements.txt
├── README.md
│
├── screenshots/
│
└── pdf_files/
```

---

# Screenshots Included

* Retrieved chunks
* Final answers
* Streamlit UI

---

# Learning Outcomes

* Understanding of RAG architecture
* Vector databases
* Document chunking
* Context-aware AI systems
* Streamlit UI development

---

# How To Run The Project

## Step 1 - Clone Repository

```bash
git clone <your_github_repo_link>
```

---

## Step 2 - Open Project Folder

```bash
cd chatbot_irinmariya/Task2
```

---

## Step 3 - Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

---

## Step 4 - Install Requirements

```bash
pip install -r requirements.txt
```

---

## Step 5 - Add Groq API Key

Open:

* `rag.py`
* `app.py`

Replace:

```python
api_key="your_api_key"
```

with your own Groq API key.

---

# Run Terminal RAG Chatbot

```bash
python rag.py
```

---

# Run Streamlit Application

```bash
streamlit run app.py
```


