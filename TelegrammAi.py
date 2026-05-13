import asyncio
import os

from openai import OpenAI
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

# -------------------
# ТОКЕН
# -------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------
# BOT
# -------------------

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

# -------------------
# START
# -------------------

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Приветcтвую Вас 😄")

# -------------------
# ECHO
# -------------------

user_histories = {}

@dp.message()
async def ai_chat(message: Message):

    user_id = message.from_user.id
    user_text = message.text

    # создаём историю
    if user_id not in user_histories:
        user_histories[user_id] = []

    # сообщение пользователя
    user_histories[user_id].append({
        "role": "user",
        "content": user_text
    })

    try:

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=user_histories[user_id]
        )

        ai_response = response.choices[0].message.content

        # сохраняем ответ AI
        user_histories[user_id].append({
            "role": "assistant",
            "content": ai_response
        })

        await message.answer(ai_response)

    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# -------------------
# RUN
# -------------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())