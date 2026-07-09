import google.generativeai as genai

from app.config import GEMINI_API_KEY
from app.database.database import database


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


async def ask_gemini(user_id: int, text: str):

    history = await database.get_history(user_id)

    prompt = ""

    for role, message in history:
        prompt += f"{role}: {message}\n"

    prompt += f"user: {text}\nassistant:"

    response = model.generate_content(prompt)

    answer = response.text

    await database.save_message(user_id, "user", text)
    await database.save_message(user_id, "assistant", answer)

    return answer
