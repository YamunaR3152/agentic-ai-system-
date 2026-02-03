# Post-Mortem Report

This document reflects on design decisions, limitations, and scalability considerations observed while building the multi-step AI system.

---

## ⚠️ Scaling Issue Encountered

**Issue:**  
As the number of user tasks increases, the system may experience delays because all tasks are processed sequentially through the same async pipeline and in-memory queues.

**Why this happens:**  
- Each task goes through multiple processing stages (retrieval → analysis → generation)  
- Model inference is computationally expensive  
- The in-memory queue does not distribute load across multiple workers  

**Impact:**  
High request volume could lead to longer response times and queue backlog.

**Future Fix:**  
- Replace in-memory queues with a distributed message broker (Redis / RabbitMQ / Kafka)  
- Add multiple worker processes to parallelize agent execution  
- Add load balancing for model inference

---

## 🔄 Design Decision I Would Change

**Current Design:**  
All agents run inside a single FastAPI application process.

**Limitation:**  
This tightly couples the agents, making it harder to scale or update them independently.

**Improved Design:**  
Each agent could run as an independent microservice communicating through a message queue.  
This would improve:
- Scalability  
- Fault isolation  
- Independent deployment  

---

## ⚖️ Trade-offs Made During Development

| Decision | Benefit | Trade-off |
|---------|---------|-----------|
| Used in-memory queues | Simple to implement | Not horizontally scalable |
| Used a small language model | Faster responses | Lower answer quality |
| Basic failure handling | System remains stable | Errors not deeply logged |
| Single-process architecture | Easier debugging | Limited production scalability |

---

## 🧠 Final Reflection

The system successfully demonstrates how multi-step tasks can be handled through coordinated components using asynchronous processing. While the current design works well for small-scale usage and demonstration purposes, future improvements would focus on distributed processing, better monitoring, and scalable infrastructure.
