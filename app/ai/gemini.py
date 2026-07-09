import google.generativeai as genai

from app.config import GEMINI_API_KEY
from app.database.database import database

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


async def ask_gemini(user_id: int, text: str):

    history = await database.get_history(user_id)
    memories = await database.get_memories(user_id)

    prompt = ""

    if memories:
        prompt += "Memory:\n"
        for key, value in memories:
            prompt += f"{key}: {value}\n"

        prompt += "\nConversation:\n"

    for role, message in history:
        prompt += f"{role}: {message}\n"

    prompt += f"user: {text}\nassistant:"

    response = model.generate_content(prompt)

    answer = response.text

    lower = text.lower()

    if "меня зовут" in lower:
        name = text.split("меня зовут", 1)[1].strip()
        await database.save_memory(user_id, "name", name)

    if "моё имя" in lower:
        name = text.split("моё имя", 1)[1].strip()
        await database.save_memory(user_id, "name", name)

    if "мой возраст" in lower:
        age = text.split("мой возраст", 1)[1].strip()
        await database.save_memory(user_id, "age", age)

    if "мне " in lower and "лет" in lower:
        await database.save_memory(user_id, "age", text)

    if "я люблю" in lower:
        likes = text.split("я люблю", 1)[1].strip()
        await database.save_memory(user_id, "likes", likes)

    if "мой город" in lower:
        city = text.split("мой город", 1)[1].strip()
        await database.save_memory(user_id, "city", city)

    if "я живу в" in lower:
        city = text.split("я живу в", 1)[1].strip()
        await database.save_memory(user_id, "city", city)

    if "моя работа" in lower:
        work = text.split("моя работа", 1)[1].strip()
        await database.save_memory(user_id, "work", work)

    if "я работаю" in lower:
        work = text.split("я работаю", 1)[1].strip()
        await database.save_memory(user_id, "work", work)

    await database.save_message(user_id, "user", text)
    await database.save_message(user_id, "assistant", answer)

    return answer
