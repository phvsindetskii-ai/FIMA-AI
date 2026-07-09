import google.generativeai as genai

from app.config import GEMINI_API_KEY
from app.database.database import database

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


async def ask_gemini(user_id: int, text: str):
    # Загружаем историю и память
    history = await database.get_history(user_id)
    memories = await database.get_memories(user_id)

    # Собираем промпт
    prompt = ""

    if memories:
        prompt += "Memory:\n"
        for key, value in memories:
            prompt += f"{key}: {value}\n"

        prompt += "\nConversation:\n"

    for role, message in history:
        prompt += f"{role}: {message}\n"

    prompt += f"user: {text}\nassistant:"

    # Ответ Gemini
    response = model.generate_content(prompt)
    answer = response.text

    # Простое сохранение фактов
    lower = text.lower()

    if "меня зовут" in lower:
        try:
            name = text.lower().split("меня зовут", 1)[1].strip().title()
            await database.save_memory(user_id, "name", name)
        except Exception:
            pass

    if "мой возраст" in lower:
        try:
            age = text.lower().split("мой возраст", 1)[1].strip()
            await database.save_memory(user_id, "age", age)
        except Exception:
            pass

    if "я люблю" in lower:
        try:
            love = text.split("я люблю", 1)[1].strip()
            await database.save_memory(user_id, "likes", love)
        except Exception:
            pass

    # Сохраняем историю
    await database.save_message(user_id, "user", text)
    await database.save_message(user_id, "assistant", answer)

    return answer
