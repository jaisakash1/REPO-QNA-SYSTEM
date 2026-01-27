# 🔍 Repo QnA - Query GitHub Repositories with Natural Language 
### 🌐 Live Demo: [https://repo-frontend-b70m.onrender.com/](https://repo-frontend-b70m.onrender.com/)

A full-stack **GenAI RAG (Retrieval Augmented Generation)** application that lets you **ask natural language questions** about any GitHub repository and get relevant code snippets as answers. Built using semantic embeddings and vector similarity search. Simply paste a GitHub URL, wait for it to be indexed, and start asking questions!

---

## 🎯 What Does This Project Do?

**Repo QnA** allows users to:

1. **Ingest any public GitHub repository** - The system clones, parses, and chunks the codebase
2. **Generate semantic embeddings** - Using Google's Gemini API (`text-embedding-004`)
3. **Search with natural language** - Query the codebase like: *"How does authentication work?"*
4. **Get relevant code snippets** - Results include file paths, line numbers, and similarity scores

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React + Vite)                    │
│  - Enter GitHub URL → Index Repository                               │
│  - Ask natural language questions → View code snippets               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           BACKEND (FastAPI)                          │
│                                                                      │
│  ┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐  │
│  │   /api/ingest   │    │   /api/query     │    │  /api/repos    │  │
│  │  Clone & Index  │    │ Semantic Search  │    │  List Indexed  │  │
│  └─────────────────┘    └──────────────────┘    └────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   ▼                ▼                ▼
            ┌───────────┐   ┌────────────────┐   ┌───────────────┐
            │  Chunking │   │   Embeddings   │   │  Vector Store │
            │ (AST/FE)  │   │ (Gemini API)   │   │   (FAISS)     │
            └───────────┘   └────────────────┘   └───────────────┘
```

---

## 🔧 Tech Stack

### Backend
| Component | Technology |
|-----------|------------|
| Framework | **FastAPI** |
| Embeddings | **Google Gemini API** (text-embedding-004) |
| Vector Database | **FAISS** (Facebook AI Similarity Search) |
| Code Parsing | **Tree-sitter** / AST-based chunking |
| Repository Cloning | **Git** |

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | **React 19** |
| Build Tool | **Vite** |
| Styling | Vanilla CSS (Dark theme with glassmorphism) |

---

## 📁 Project Structure

```
REPO_QNA/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── routes/
│   │   │   ├── ingest.py        # POST /api/ingest - Clone & index repos
│   │   │   └── query.py         # POST /api/query - Semantic search
│   │   └── utils/
│   │       └── code_fetcher.py  # Retrieve code from chunks
│   │
│   ├── ingestion/
│   │   ├── pipeline.py          # Main ingestion orchestration
│   │   ├── clone_repo.py        # Git clone logic
│   │   └── extract_files.py     # Extract source files
│   │
│   ├── chunking/
│   │   ├── chunk_resolver.py    # Resolve chunks (AST + fallback)
│   │   ├── function_extractor.py # Extract functions/classes
│   │   └── save_chunks.py       # Persist chunks to JSON
│   │
│   ├── embeddings/
│   │   └── generate_embeddings_local.py  # Gemini API embeddings
│   │
│   ├── vector_store/
│   │   └── faiss_store.py       # FAISS index creation & search
│   │
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile               # Backend containerization
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   └── App.css              # Styling
│   ├── package.json             # Node dependencies
│   └── vite.config.js           # Vite configuration
│
├── data/
│   ├── repos/                   # Cloned repositories (temp)
│   ├── chunks/                  # Saved code chunks (JSON)
│   └── embeddings/              # Generated embeddings
│
├── vector_store/                # FAISS indices per repo
│   └── {repo_name}_faiss.index
│
└── .env                         # Environment variables
```

---

## 🚀 How It Works

### **Step 1: Ingestion Pipeline** (`POST /api/ingest`)

When a GitHub URL is submitted:

1. **Clone Repository** - Uses `git clone` to download the repo
2. **Extract Files** - Filters for supported code files
3. **Chunk Code** - Uses AST parsing to extract functions/classes (with fallback to line-based chunking)
4. **Generate Embeddings** - Sends chunks to Gemini API for semantic embeddings
5. **Create FAISS Index** - Stores vectors for fast similarity search
6. **Save Chunks** - Persists code chunks to JSON for retrieval
7. **Cleanup** - Deletes cloned repo (only chunks & index are kept)

### **Step 2: Query Pipeline** (`POST /api/query`)

When a natural language question is asked:

1. **Generate Query Embedding** - Convert question to vector using Gemini
2. **FAISS Search** - Find top-k most similar code chunks
3. **Retrieve Code** - Fetch actual source code from saved chunks
4. **Return Results** - Include file path, line numbers, similarity score, and code

---

## ⚙️ Setup & Installation

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Git**
- **Google Gemini API Key** (for embeddings)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variable
# Create .env file with:
GEMINI_API_KEY=your_api_key_here

# Run the server
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file with:
VITE_API_URL=http://localhost:8000/api

# Run development server
npm run dev
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info & available endpoints |
| `GET` | `/health` | Health check |
| `POST` | `/api/ingest` | Ingest a GitHub repository |
| `POST` | `/api/query` | Query repository with natural language |
| `GET` | `/api/repos` | List all indexed repositories |

### Example: Ingest a Repository

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/username/repo"}'
```

### Example: Query a Repository

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"repo_name": "repo", "query": "How does user authentication work?", "top_k": 5}'
```

---

## 🚢 Deployment

### Backend (Render)

The project includes a `render.yaml` and `Dockerfile` for easy deployment to [Render](https://render.com).

### Frontend (Vercel)

Deploy the frontend to [Vercel](https://vercel.com) with:
- Set `VITE_API_URL` to your deployed backend URL

---

## 🔑 Environment Variables

### Backend (`.env`)
```
GEMINI_API_KEY=your_gemini_api_key
```

### Frontend (`.env`)
```
VITE_API_URL=http://localhost:8000/api
```

---

## ✨ Features

- ✅ **Natural language search** - Ask questions in plain English
- ✅ **AST-based code chunking** - Intelligent function/class extraction
- ✅ **Semantic similarity** - Powered by Gemini embeddings
- ✅ **Fast vector search** - Using FAISS for efficient lookup
- ✅ **Multi-language support** - Python, JavaScript, TypeScript, Java, C++, and more
- ✅ **Automatic cleanup** - Cloned repos are deleted after indexing
- ✅ **Skip re-indexing** - Already indexed repos are detected automatically
- ✅ **Dark mode UI** - Modern, responsive interface with animations

---

## 📝 License

This project is for educational and personal use.

---

## 🤝 Contributing

Feel free to submit issues and pull requests to improve the project!
