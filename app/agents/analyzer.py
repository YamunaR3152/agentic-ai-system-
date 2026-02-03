import asyncio
from sentence_transformers import util
from app.preprocessing.embedding_loader import EMBEDDING_MODEL
from app.core.task_queue import (
    RETRIEVER_QUEUE,
    ANALYZER_QUEUE,
    STATUS_QUEUE,
    pop_task,
    push_task
)

class AnalyzerAgent:
    async def run(self):
        print("🚀 Analyzer Agent started")

        while True:
            task = pop_task(RETRIEVER_QUEUE)

            if not task:
                await asyncio.sleep(0.5)
                continue

            task_id = task.get("task_id")
            text = task.get("retrieved_text", "")
            full_query = task.get("query", "")

            push_task(STATUS_QUEUE, {
                "task_id": task_id,
                "type": "status",
                "message": "🧠 Analyzing retrieved knowledge..."
            })

            if not text or text.startswith("❌"):
                task["analysis"] = text
                push_task(ANALYZER_QUEUE, task)
                continue

            questions = [q.strip() for q in full_query.split("?") if q.strip()]
            sentences = [
                s.strip() for s in text.replace("\n", " ").split(".")
                if len(s.strip()) > 40
            ]

            if not sentences:
                task["analysis"] = ["❌ No meaningful content found."]
                push_task(ANALYZER_QUEUE, task)
                continue

            sent_emb = EMBEDDING_MODEL.encode(sentences, convert_to_tensor=True)
            results = []

            for q in questions:
                q_lower = q.lower()

                # 🎯 TOPIC KEYWORDS
                if "artificial intelligence" in q_lower or q_lower.endswith(" ai"):
                    keywords = ["artificial intelligence", " ai "]
                elif "machine learning" in q_lower:
                    keywords = ["machine learning", " ml "]
                elif "data science" in q_lower and "trend" in q_lower:
                    keywords = [
                        "trend", "future", "emerging", "growth", "advancement",
                        "automation", "big data", "ai integration"
                    ]
                elif "type" in q_lower:
                    keywords = ["type", "category", "narrow ai", "general ai", "super ai"]
                else:
                    keywords = []

                # 🔎 Strict filtering first
                filtered_sentences = [
                    s for s in sentences if any(k in s.lower() for k in keywords)
                ]

                # fallback if nothing matched
                if not filtered_sentences:
                    filtered_sentences = sentences

                filtered_emb = EMBEDDING_MODEL.encode(filtered_sentences, convert_to_tensor=True)
                query_emb = EMBEDDING_MODEL.encode(q, convert_to_tensor=True)

                scores = util.cos_sim(query_emb, filtered_emb)[0]
                top_k = min(4, len(filtered_sentences))
                top_indices = scores.topk(top_k).indices.tolist()

                # 🚫 Remove duplicates + cross-topic pollution
                unique_points = []
                for i in top_indices:
                    sent = filtered_sentences[i]

                    if sent in unique_points:
                        continue

                    # block ML sentence in AI answer
                    if "machine learning" in sent.lower() and "machine learning" not in q_lower:
                        continue

                    # block AI definition in trends question
                    if "artificial intelligence (ai) is" in sent.lower() and "trend" in q_lower:
                        continue

                    unique_points.append(sent)

                results.append({
                    "question": q,
                    "points": unique_points[:3]
                })

            task["analysis"] = results
            push_task(ANALYZER_QUEUE, task)
