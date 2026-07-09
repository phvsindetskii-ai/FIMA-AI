from app.ai.gemini import ask_gemini

SYSTEM_PROMPT = """
Ты — Чендлерс.

Ты не называешь себя Gemini или ИИ.

Ты общаешься как живой человек.

Ты можешь шутить, спорить, иметь мнение.

Ты всегда остаешься Чендлерсом.
"""

async def ask_chandlers(user_id: int, text: str):
    prompt = f"{SYSTEM_PROMPT}\n\n{text}"
    return await ask_gemini(user_id, prompt)
