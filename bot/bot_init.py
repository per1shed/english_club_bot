from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    PicklePersistence,
)
from config.config import TELEGRAM_TOKEN
from config.states import START, JOIN_CLUB, PAYMENT
from bot.handlers.start_handler import start, button_handler, cancel
from logs.logger import logger

def init_bot():
    persistence = PicklePersistence("bot_cache")
    application = (
        Application.builder().token(TELEGRAM_TOKEN).persistence(persistence).build()
    )
    logger.info("Запуск тг бота ✅")
    
    # Создаем ConversationHandler для клуба
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [CallbackQueryHandler(button_handler)],
            JOIN_CLUB: [CallbackQueryHandler(button_handler)],
            PAYMENT: [CallbackQueryHandler(button_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="club_conversation",
        persistent=True,
    )
    
    application.add_handler(conv_handler)
    return application