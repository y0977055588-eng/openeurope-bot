import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")

ADMINS = {
    "OE_PL": [111111111],
    "OE_DE": [222222222],
    "OE_UK": [333333333],
    "DEFAULT": [111111111]
}

bot = Bot(TOKEN)
dp = Dispatcher()

user_context = {}

@dp.message(Command("start"))
async def start_handler(message: Message):
    args = message.text.split()
    group_code = args[1] if len(args) > 1 else "DEFAULT"

    user_context[message.from_user.id] = {"group": group_code}

    await message.answer(
        "👋 Вітаємо!\n\n"
        "Напишіть, будь ласка, ваше повідомлення.\n"
        "Воно буде передано адміністрації."
    )

@dp.message(F.chat.type == "private")
async def user_message(message: Message):
    user_id = message.from_user.id

    if user_id not in user_context:
        await message.answer("❗ Натисніть /start для початку.")
        return

    group = user_context[user_id]["group"]
    admins = ADMINS.get(group, ADMINS["DEFAULT"])

    for admin_id in admins:
        await bot.send_message(
            admin_id,
            f"📩 Новий запит\n\n"
            f"👥 Група: {group}\n"
            f"👤 Користувач: @{message.from_user.username}\n"
            f"🆔 ID: {user_id}\n\n"
            f"💬 Повідомлення:\n{message.text}"
        )

    await message.answer("✅ Повідомлення передано адміну.")

@dp.message(F.reply_to_message)
async def admin_reply(message: Message):
    if message.from_user.id not in sum(ADMINS.values(), []):
        return

    try:
        lines = message.reply_to_message.text.splitlines()
        user_id = int([l for l in lines if l.startswith("🆔")][0].split(":")[1])
        await bot.send_message(
            user_id,
            f"💬 Відповідь адміністрації:\n\n{message.text}"
        )
    except:
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
