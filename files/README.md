<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=378ADD&center=true&vCenter=true&width=940&lines=🤖+IntraBot+–+Domain+Specific+Chatbot;Offline+AI+%7C+RAG+Architecture+%7C+Zero+Hallucinations;Your+Documents.+Your+Data.+Your+Machine." alt="IntraBot" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG%20Pipeline-1C3C3C?style=for-the-badge)](https://langchain.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20DB-4285F4?style=for-the-badge)](https://faiss.ai)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge)](https://ollama.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![100% Offline](https://img.shields.io/badge/100%25-Offline-success?style=for-the-badge)]()

<br/>

> **🔒 Zero cloud. Zero hallucinations. Zero privacy risk.**
>
> *An intelligent offline AI chatbot that answers questions directly from your organizational documents — running entirely on your machine.*

<br/>

[🚀 Quick Start](#-getting-started) &nbsp;·&nbsp; [📸 Screenshots](#-screenshots) &nbsp;·&nbsp; [🏗️ Architecture](#%EF%B8%8F-architecture) &nbsp;·&nbsp; [⚙️ Config](#%EF%B8%8F-configuration) &nbsp;·&nbsp; [🔌 API Docs](#-api-reference)

</div>

---

## 📸 Screenshots

<div align="center">

### 💬 Chat Interface — Ask anything from your documents

![IntraBot Chat Interface](screenshot_chat.png)

*Query your HR documents in natural language — every answer is grounded strictly in your uploaded files*

<br/>

### 📁 Knowledge Base — Manage your documents

![Knowledge Base Sidebar](screenshot_sidebar.png)

*Upload PDFs, DOCX, TXT, CSV files — switch between documents or query all at once*

</div>

---

## 🧠 What is IntraBot?

**IntraBot** is a **Retrieval-Augmented Generation (RAG)** powered chatbot built for enterprise and organizational use. It lets you upload internal documents — HR policies, employee handbooks, leave guides, onboarding manuals — and ask questions in plain English, getting **precise, grounded answers without sending your data to any cloud service**.

```
User asks:  "How many sick leaves am I entitled to?"

IntraBot:   📂 Searches YOUR uploaded HR docs
            ✂️  Finds top-3 most relevant chunks via FAISS
            📝 Builds prompt with context + question
            🤖 Local LLM generates grounded answer
            ✅ Returns accurate, document-based response
```

### Why IntraBot over ChatGPT / cloud AI?

| Feature | ❌ Cloud AI (ChatGPT etc.) | ✅ IntraBot |
|---|---|---|
| Data Privacy | Sent to external servers | Stays on your machine |
| Hallucinations | Makes up answers | Grounded in your docs only |
| Internet Needed | Yes, always | 100% Offline |
| Cost | Subscription / API fees | Free & Open Source |
| Domain Accuracy | Generic responses | From your actual policies |
| Setup | Instant | One-time local setup |

---

## ✨ Key Features

```
🔒  100% Offline        →  No data ever leaves your machine
🧠  RAG Architecture    →  Retrieve first, then generate — grounded answers
🚫  Hallucination Guard →  LLM answers ONLY from retrieved document context
⚡  Query Caching       →  Repeated questions answered in <50ms from cache
📄  Multi-Format        →  PDF · DOCX · TXT · CSV — all formats supported
🎯  Per-Doc Filtering   →  Query all docs or target one specific file
🌐  REST API            →  Clean FastAPI endpoints for external integrations
🎨  Modern UI           →  NiceGUI Claymorphism interface with Aurora animations
```

---

## 🏗️ Architecture

### Complete System Flow

```
╔══════════════════════════════════════════════════════════════════╗
║                 📥 DOCUMENT INGESTION PIPELINE                    ║
╠══════════════════════════════════════════════════════════════════╣
║  📄 Upload → 🔍 Extract Text → ✂️ Chunk (300 chars) → 🔢 Embed   ║
║                                          ↓                        ║
║                                   💾 FAISS Vector DB              ║
╚══════════════════════════════════════════════════════════════════╝
                                          ↕
╔══════════════════════════════════════════════════════════════════╗
║                   ❓ QUERY ANSWERING PIPELINE                     ║
╠══════════════════════════════════════════════════════════════════╣
║  ❓ User Query → 🔢 Embed Query → 🔍 FAISS Similarity Search      ║
║       ↓                                    ↓                     ║
║  ⚡ Cache Hit? ←──── 📋 Top-K Chunks ────→ 📝 Build RAG Prompt    ║
║       ↓ (instant)                          ↓                     ║
║  💬 Return Answer ←───────── 🤖 Ollama (TinyLlama / Phi-3)       ║
╚══════════════════════════════════════════════════════════════════╝
```

### Project Structure

```
intrabot/
│
├── 📄 app/
│   ├── main.py                  ← FastAPI entry point + API routes
│   ├── services/
│   │   ├── ingestion.py         ← Document loading + chunking pipeline
│   │   ├── vector_store.py      ← FAISS index management
│   │   └── rag_service.py       ← RAG query + hallucination prevention
│   └── utils/
│       ├── config.py            ← All configuration constants
│       ├── embeddings.py        ← Singleton embedding model loader
│       └── cache_utils.py       ← MD5-keyed JSON response cache
│
├── 📂 data/                     ← Uploaded documents  [gitignored]
├── 📂 vectorstore/              ← FAISS index files   [gitignored]
├── 📂 cache/                    ← Cached responses    [gitignored]
├── 📂 myenv/                    ← Virtual environment [gitignored]
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core backend implementation |
| **Backend API** | FastAPI + Uvicorn | REST endpoints, async handling |
| **Frontend UI** | NiceGUI | Python-first web interface |
| **RAG Orchestration** | LangChain | Doc loaders, chunking, retrieval |
| **Embeddings** | Sentence Transformers `all-MiniLM-L6-v2` | 384-dim semantic vectors |
| **Vector Database** | FAISS (Facebook AI) | Local vector similarity search |
| **LLM Runtime** | Ollama | Local model inference engine |
| **Language Models** | TinyLlama 1.1B · Phi-3 3.8B | Answer generation |
| **Doc Parsers** | PyPDF · Docx2txt · TextLoader · CSVLoader | Multi-format support |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- [Ollama](https://ollama.ai) installed and running
- **8 GB RAM** minimum (16 GB recommended)
- ~5 GB free disk space for models

### 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/intrabot.git
cd intrabot
```

### 2 — Create virtual environment

```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# macOS / Linux
source myenv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Pull a local LLM via Ollama

```bash
# Option A — Lightweight (recommended for most CPUs)
ollama pull tinyllama

# Option B — Better quality (needs more RAM)
ollama pull phi3
```

### 5 — Start the application

```bash
# Terminal 1 — FastAPI backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 — NiceGUI frontend
python app/ui/main_ui.py
```

### 6 — Open in browser

```
http://localhost:8080
```

> 🎉 Upload a document, ask a question, get an accurate offline answer!

---

## ⚙️ Configuration

Edit `app/utils/config.py` to customize behaviour:

```python
# ── RAG Pipeline ─────────────────────────────────────────────────────
CHUNK_SIZE            = 300    # Characters per chunk
CHUNK_OVERLAP         = 45     # 15% overlap — preserves context at boundaries
MIN_CHUNK_SIZE        = 5      # Minimum words — short chunks are discarded

# ── Embedding Model ───────────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
#                  └── 384-dimensional vectors, CPU-optimized

# ── LLM Settings ─────────────────────────────────────────────────────
LLM_MODEL             = "tinyllama:latest"   # swap to "phi3" for better quality
OLLAMA_BASE_URL       = "http://localhost:11434"
TEMPERATURE           = 0.7
MAX_TOKENS            = 300

# ── Retrieval Settings ────────────────────────────────────────────────
RETRIEVAL_TOP_K       = 3      # Chunks passed into the LLM prompt
RERANK_TOP_K          = 5      # Candidates before re-ranking
SIMILARITY_THRESHOLD  = 0.4    # Min similarity score — lower = more results
```

---

## 🔌 API Reference

### Upload Documents

```http
POST /upload
Content-Type: multipart/form-data
```

```bash
curl -X POST "http://localhost:8000/upload" \
     -F "files=@HR_Policy_Manual.pdf" \
     -F "files=@Leave_Rules.docx"
```

**Response:**
```json
{ "message": "Successfully indexed 2 documents." }
```

---

### Query the Knowledge Base

```http
POST /query
Content-Type: application/json
```

```bash
# Search ALL documents
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How many sick leaves am I entitled to?", "document_name": null}'

# Search ONE specific document
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the notice period?", "document_name": "HR_Policy_Manual.pdf"}'
```

**Response:**
```json
{
  "answer": "Employees are entitled to 10 days of paid sick leave per calendar year. For absences longer than 3 days, a medical certificate is required...",
  "sources": ["HR_Policy_Manual.pdf"]
}
```

**Fallback (when info not found):**
```json
{
  "answer": "Information not found in documents",
  "sources": []
}
```

---

## 🚫 How Hallucination Prevention Works

IntraBot uses a strict prompt template that **explicitly forbids fabrication**:

```python
# From rag_service.py
template = """
You are IntraBot, a local HR assistant.
Use ONLY the following context to answer the user's question.
If the answer is NOT in the context, say EXACTLY:
"Information not found in documents"
Do NOT use external knowledge. Do NOT hallucinate.

Context: {context}
Question: {question}
Answer:"""
```

**Three-layer protection system:**

```
Layer 1 → FAISS threshold (0.4)   — low-relevance chunks are discarded
Layer 2 → No chunks found?        — return fallback, LLM is never called  
Layer 3 → Strict prompt rule      — LLM forbidden from using outside knowledge
```

---

## 📊 Performance Metrics

| Metric | Value |
|---|---|
| Embedding model size | ~90 MB |
| Vector dimensions | 384 (all-MiniLM-L6-v2) |
| Query latency (cached) | < 50ms |
| Query latency (TinyLlama, CPU) | 5–15 seconds |
| Query latency (Phi-3, CPU) | 15–40 seconds |
| Max document size | ~500 pages per upload |
| Chunk size | 300 characters with 45-char overlap |

---

## 🧪 Test Results

| Test Case | Input | Expected | Result |
|---|---|---|---|
| TC-01 | Upload PDF | Successful ingestion | ✅ Pass |
| TC-02 | Upload DOCX | Text extraction | ✅ Pass |
| TC-03 | Semantic query | Relevant response | ✅ Pass |
| TC-04 | Unknown question | Fallback returned | ✅ Pass |
| TC-05 | Repeated query | Cached response | ✅ Pass |
| TC-06 | Invalid file format | Validation error | ✅ Pass |
| TC-07 | Offline (no internet) | Fully operational | ✅ Pass |
| TC-08 | REST API call | JSON response | ✅ Pass |

---

## 🔮 Roadmap

- [ ] 🔐 Role-based multi-user authentication
- [ ] 📷 OCR support for scanned PDFs and image-based documents
- [ ] 🎙️ Voice input / text-to-speech output
- [ ] 📊 Admin analytics dashboard
- [ ] 🌍 Multilingual document and query support
- [ ] 🦙 Llama-3 / Mistral-7B / DeepSeek model support
- [ ] 🏢 SharePoint / Confluence / HRMS integration
- [ ] 📱 Mobile application
- [ ] ⚡ GPU acceleration

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork → Clone → Branch → Commit → Pull Request

git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Abhinav Sharma** &nbsp;|&nbsp; Roll No: 2206286

B.Tech Computer Science Engineering  
Rayat Bahra Institute of Engineering & Nano-Technology, Hoshiarpur  
*Six Months Industrial Training Project — May 2026*

---

## 📚 References

1. Lewis, P. et al. — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020
2. [FastAPI Documentation](https://fastapi.tiangolo.com)
3. [LangChain Documentation](https://docs.langchain.com)
4. [FAISS — Facebook AI Research](https://faiss.ai)
5. [Sentence Transformers — Reimers & Gurevych, EMNLP 2019](https://sbert.net)
6. [Ollama Documentation](https://ollama.ai)
7. [NiceGUI Documentation](https://nicegui.io)
8. [Microsoft Phi-3](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct)
9. [TinyLlama](https://github.com/jzhang38/TinyLlama)
10. [Python Documentation](https://docs.python.org)

---

<div align="center">

**⭐ If IntraBot helped you, please star this repo! ⭐**

<br/>

*Built with ❤️ using Python · LangChain · FAISS · Ollama · FastAPI*

</div>
