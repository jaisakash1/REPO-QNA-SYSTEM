# LinkedIn Post for Repo QnA

---

## Option 1: Problem-Solution Hook 🎯 (WITH TECHNICAL DEPTH)

**Ever spent HOURS searching through an unfamiliar codebase just to understand "where does this function even get called?"**

We've all been there. 😩

You join a new project. 10,000+ lines of code. Zero documentation. And your task? "Just add this small feature."

So I built something to fix this 👇

**Introducing Repo QnA** — A GenAI RAG system that lets you ask natural language questions about ANY GitHub repository.

🔹 Paste a GitHub URL
🔹 Wait 30 seconds for indexing
🔹 Ask questions like:
   - "How does authentication work?"
   - "Where is the database connection handled?"
   - "What does the payment flow look like?"

And boom 💥 — you get the EXACT code snippets with file paths and line numbers.

---

**🧠 The Secret Sauce: Intelligent Code Chunking**

Most RAG systems chunk text by fixed line counts. But code isn't text — it's structured.

So I used **Tree-sitter** — a powerful AST parsing library — to intelligently extract **functions, classes, and methods** as individual chunks.

Why does this matter?

→ A 50-line function stays together (not split randomly)
→ Each chunk has semantic meaning
→ Retrieval returns complete, usable code blocks

**Supports 15+ languages out of the box:**
Python, JavaScript, TypeScript, Java, Go, C, C++, Kotlin, Swift, Ruby, PHP, and more!

Each language has different function syntax — Tree-sitter handles them all with language-specific parsers. 🎯

---

**📊 The Full Pipeline:**

```
GitHub URL
    ↓
Clone Repo → Parse with Tree-sitter (AST)
    ↓
Extract Functions/Classes as Chunks
    ↓
Generate Embeddings (Gemini text-embedding-004)
    ↓
Store in FAISS Vector Index
    ↓
Query → Semantic Search → Return Code
```

---

**The Tech Stack:**
⚡ FastAPI backend
⚡ React frontend (dark theme + glassmorphism)
⚡ Tree-sitter for AST-based code parsing
⚡ FAISS for vector similarity search
⚡ Google Gemini API (`text-embedding-004`) for embeddings

🔗 **Try the Live Demo:** https://repo-frontend-b70m.onrender.com/
📂 **GitHub Repo:** [Add your GitHub repo link here]

Built this over a weekend. Still learning and iterating — there may be some rough edges, but feedback is always welcome! 🙌

What repo should I test this on? Drop a link below! 👇

#GenAI #RAG #MachineLearning #OpenSource #Python #React #Developers #Coding #TreeSitter #FAISS #Embeddings #BuildInPublic

---

## Option 2: Story-Based Hook 📖

**"Just read the code" — The 3 worst words in software development.**

Last month, I was onboarding onto a legacy Django project.

2 hours in, I was still doing Ctrl+F trying to find where user sessions get validated.

That's when I thought: **What if I could just ASK the codebase?**

So I built it. 🚀

**Repo QnA** — Paste any GitHub repo link, and ask questions in plain English.

✅ "How is the API rate limiting implemented?"
✅ "Where are environment variables loaded?"
✅ "Show me the main entry point of this app"

No more grep. No more endless Ctrl+clicking. Just answers.

**How it works:**
1️⃣ Clones your repo
2️⃣ Chunks code into semantic blocks (AST-based)
3️⃣ Generates embeddings using Gemini
4️⃣ Stores in FAISS for lightning-fast search
5️⃣ Returns relevant code with similarity scores

**Try it NOW (it's free):**
🔗 https://repo-frontend-b70m.onrender.com/

Would love your feedback! What repos should I test this on? 👇

#RAG #GenerativeAI #Python #React #FAISS #Embeddings #Developers #OpenSource

---

## Option 3: Short & Punchy 🔥

**Stop reading code. Start asking it questions.**

I built a RAG system that lets you query ANY GitHub codebase in plain English.

🔍 Paste a repo URL
💬 Ask: "How does the auth middleware work?"
📄 Get: The exact code + file path + line numbers

No setup. No API keys needed. Just try it:
👉 https://repo-frontend-b70m.onrender.com/

Built with FastAPI, React, FAISS & Gemini Embeddings.

GitHub coming soon! 🚀

#GenAI #RAG #Python #React #BuildInPublic

---

## Option 4: For Maximum Engagement 📈

**I was mass rejected from tech jobs for not having "real projects."**

So I built this over the weekend. 👇

**Repo QnA** — A GenAI RAG app that lets you search codebases using natural language.

The problem it solves:
→ New developer joins a 50k line codebase
→ Spends 3 days just understanding the structure
→ Still doesn't know where half the logic lives

My solution:
→ Paste any GitHub URL
→ Ask "How does X work?"
→ Get exact code snippets with file locations

**Under the hood:**
🔸 Clone repo → Parse with AST → Chunk code
🔸 Generate embeddings (Gemini text-embedding-004)
🔸 Store in FAISS vector database
🔸 Semantic search with similarity scores

**Live demo (try it!):**
🔗 https://repo-frontend-b70m.onrender.com/

What repo should I test this on? Drop a link below! 👇

#GenAI #RAG #Python #FastAPI #React #MachineLearning #Embeddings #OpenSource #BuildInPublic #TechCareers

---

## Pro Tips for LinkedIn Reach:

1. **Post between 8-10 AM** on Tuesday/Wednesday/Thursday
2. **Reply to every comment** in the first 2 hours
3. **Ask a question** at the end to drive engagement
4. **Use emojis** but don't overdo it
5. **Add a carousel image** showing the UI (increases reach 2x)
6. **Tag relevant people** who might reshare

---
