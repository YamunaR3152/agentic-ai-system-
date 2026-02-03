import asyncio
from app.core.task_queue import ANALYZER_QUEUE, STATUS_QUEUE, pop_task, push_task


class WriterAgent:
    async def run(self):
        print("🚀 Writer Agent started")

        while True:
            task = pop_task(ANALYZER_QUEUE)

            if not task:
                await asyncio.sleep(0.5)
                continue

            task_id = task.get("task_id")
            analysis = task.get("analysis")

            push_task(STATUS_QUEUE, {
                "task_id": task_id,
                "type": "status",
                "message": "✍️ Writing final answer..."
            })

            # ❌ If retrieval failed earlier
            if not analysis or isinstance(analysis, str):
                final_answer = analysis if analysis else "❌ No data retrieved"
            else:
                # ✅ Build answer question by question
                output_lines = []

                for item in analysis:
                    question = item.get("question", "").strip()
                    points = item.get("points", [])

                    output_lines.append(f"🔹 {question}?")

                    if not points:
                        output_lines.append("• No relevant information found.")
                    else:
                        for p in points:
                            output_lines.append(f"• {p.strip()}")

                    output_lines.append("")  # spacing

                final_answer = "\n".join(output_lines)

            # ✅ Send final output
            push_task(STATUS_QUEUE, {
                "task_id": task_id,
                "type": "final",
                "message": final_answer
            })
