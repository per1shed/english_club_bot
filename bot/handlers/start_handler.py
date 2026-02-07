from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, contect: ContextTypes.DEFAULT_TYPE) -> int:
    await contect.bot.send_message(
        chat_id=update._effective_chat.id,
        text="Привет! я бот для управления вашим ботом"
    )