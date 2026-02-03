import uuid
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.core.task_queue import TASK_QUEUE, STATUS_QUEUE, push_task, pop_task
from app.agents.retriever import RetrieverAgent
from app.agents.analyzer import AnalyzerAgent
from app.agents.writer import WriterAgent

app = FastAPI()

# 📁 Templates & Static setup
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 🧠 Store status history per task
TASK_STATUS_HISTORY = {}


# 🚀 Start AI Agents on server startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(RetrieverAgent().run())
    asyncio.create_task(AnalyzerAgent().run())
    asyncio.create_task(WriterAgent().run())


class QueryRequest(BaseModel):
    query: str


# 🏠 Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 📩 Submit Task
@app.post("/submit-task")
def submit_task(req: QueryRequest):
    task_id = str(uuid.uuid4())

    TASK_STATUS_HISTORY[task_id] = []  # initialize history

    push_task(TASK_QUEUE, {
        "task_id": task_id,
        "query": req.query
    })

    return {"task_id": task_id}


# 📊 Get Task Status Updates
@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    # Collect new messages from queue
    while True:
        msg = pop_task(STATUS_QUEUE)
        if not msg:
            break

        tid = msg["task_id"]
        if tid not in TASK_STATUS_HISTORY:
            TASK_STATUS_HISTORY[tid] = []

        TASK_STATUS_HISTORY[tid].append(msg)

    history = TASK_STATUS_HISTORY.get(task_id, [])

    if not history:
        return {"type": "status", "message": "⏳ Processing..."}

    return history[-1]  # return latest, frontend stacks them visually
