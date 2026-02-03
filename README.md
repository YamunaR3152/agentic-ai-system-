# 📚 Agentic AI Research System

An Agent-based AI research assistant that can take user questions, retrieve knowledge, analyze it, and generate structured answers using multiple AI agents working together.

---

## 🚀 Project Overview

This system simulates **Agentic AI architecture**, where multiple AI agents collaborate to solve a task:

1. **Retriever Agent** → Finds relevant knowledge  
2. **Analyzer Agent** → Filters & organizes information  
3. **Writer Agent** → Generates final structured answers  

The system runs on **FastAPI** and processes tasks asynchronously using internal queues.

---

## 🧠 Technologies Used

| Layer | Technology |
|------|------------|
| Backend API | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| AI Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| Language Model | FLAN-T5 (HuggingFace Transformers) |
| Data Validation | Pydantic |
| Async Processing | Python asyncio |

---

## 🏗️ Project Structure

```
app/
│
├── main.py                # FastAPI entry point
│
├── core/
│   └── task_queue.py      # Task & status queue system
│
├── agents/
│   ├── retriever.py       # Retrieves knowledge
│   ├── analyzer.py        # Filters & processes data
│   └── writer.py          # Generates final answer
│
├── templates/
│   └── index.html         # Frontend UI
│
└── static/
    ├── style.css          # Styling
    └── main.js            # Frontend logic
```

---

## 🔄 System Data Flow (Architecture)

```
User Question
      ↓
Frontend (index.html + JS)
      ↓
FastAPI Endpoint (/submit-task)[where the task is stored in the Redis 
      ↓
TASK_QUEUE ───────────────► Retriever Agent
                              ↓
                         Analyzer Agent
                              ↓
                          Writer Agent
                              ↓
STATUS_QUEUE ◄────────────────────┘
      ↓
Frontend polls /task-status/{task_id}
      ↓
Final Answer Displayed
```

---

## ⚙️ How It Works (Step-by-Step)

### 1️⃣ User submits a query

The frontend sends the question to:

```
POST /submit-task
```

A unique **task_id** is generated and pushed into the task queue.

---

### 2️⃣ Retriever Agent

- Converts documents into embeddings  
- Uses FAISS to find relevant knowledge  
- Fetches additional knowledge from Wikipedia  
- Sends retrieved text to the Analyzer Agent  

---

### 3️⃣ Analyzer Agent

- Removes irrelevant information  
- Filters sentences based on question topic  
- Prevents cross-topic mixing (AI vs ML vs Data Science)  
- Sends clean knowledge to Writer Agent  

---

### 4️⃣ Writer Agent

- Uses FLAN-T5 model  
- Generates structured bullet-point answers  
- Pushes final output to STATUS_QUEUE  

---

### 5️⃣ Frontend Polling

Frontend keeps checking:

```
GET /task-status/{task_id}
```

Once completed, the answer is displayed.

---

## 🛡️ Failure Handling & System Reliability

In an Agentic AI system, multiple agents work independently. If one agent fails, the system should **not crash**. This project includes basic failure handling to maintain system stability.

### ⚠️ Possible Failure Points

| Stage | Possible Issue | Handling Strategy |
|------|----------------|------------------|
| Retriever Agent | No relevant documents found | Sends `"No data retrieved"` instead of crashing |
| Wikipedia Fetch | API/network failure | Skips Wikipedia and continues with local data |
| Analyzer Agent | No relevant sentences | Passes original retrieved text forward |
| Writer Agent | Model generation error | Returns a fallback response |
| Queue System | Empty queue | Agents wait using async sleep instead of stopping |

---

### 🔄 Graceful Degradation

If any step fails, the system still provides **partial results** rather than stopping completely.

**Examples:**

- If Wikipedia fails → Local documents are still used  
- If filtering fails → Raw retrieved data is still summarized  
- If generation fails → Error-safe message returned  

---

### 🧠 Why This Matters

Agent systems are distributed and asynchronous.

Without failure handling:  
❌ One agent crash → Whole system stops  

With failure handling:  
✅ Other agents continue working  
✅ User still gets a response  
✅ System remains stable  

---

### 🧩 Future Reliability Improvements

- Add retry mechanism for failed API calls  
- Add timeout handling for long model responses  
- Add logging system to track agent failures  
- Add monitoring dashboard for task health  

---

## 🖥️ Running the Project

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start the server

```bash
uvicorn app.main:app --reload
```

### 3️⃣ Open in browser

```
http://127.0.0.1:8000
```

---

## 🎯 Key Features

✅ Multi-agent AI pipeline  
✅ Async background task processing  
✅ Retrieval-Augmented Generation (RAG)  
✅ Topic-aware filtering to prevent wrong answers  
✅ Clean frontend with live task updates  
✅ Fault-tolerant agent workflow  

---

## 🔮 Future Improvements

- Add document upload support  
- Add conversation memory  
- Improve ranking of retrieved chunks  
- Use larger LLM for richer answers  

---

## 👩‍💻 Built For

This project demonstrates **Agentic AI + RAG architecture** for academic and research purposes.

---

