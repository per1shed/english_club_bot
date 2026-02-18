from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes, ConversationHandler
from config.states import START, JOIN_CLUB, PAYMENT
from config.config import WEBHOOK_URL, WEBAPP_PATH

# Описание клуба
CLUB_DESCRIPTION = """
🎯 *Добро пожаловать в English Club Bot!*

Мы создали идеальное пространство для изучения английского:
• 📚 Эксклюзивные материалы и уроки
• 🗣️ Практика с носителями языка
• 👥 Комьюнити единомышленников
• 🎯 Личный прогресс и отслеживание

Присоединяйся к нам и прокачай свой английский!
"""

# Преимущества клуба
BENEFITS_TEXT = """
🔥 *Преимущества нашего English Club:*

✅ *Эксклюзивный контент*:
   - Ежедневные уроки и упражнения
   - Закрытые вебинары с носителями
   - Персональные планы обучения

✅ *Практика*:
   - Разговорные клубы
   - Коррекция произношения
   - Письменные задания с проверкой

✅ *Поддержка*:
   - Куратор 24/7
   - Групповые чаты по уровням
   - Совместные проекты

🎁 *Бонус для новых участников*:
   - Неделя бесплатного доступа
   - Диагностика уровня
   - Персональный план обучения
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /start - главное меню"""
    # Создаем inline-клавиатуру
    keyboard = [
        [
            InlineKeyboardButton("Вступить в клуб", callback_data="join_club"),
            InlineKeyboardButton("Зачем тебе в клуб", callback_data="why_club"),
        ],
        [
            InlineKeyboardButton("Поддержка", url="https://t.me/+lnXg7LoeBgg2MzY6"),
            InlineKeyboardButton("Отзывы", url="https://t.me/+IOifOfhVPnw4MTEy"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=CLUB_DESCRIPTION, reply_markup=reply_markup, parse_mode="Markdown"
    )
    return START


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик inline-кнопок"""
    query = update.callback_query
    await query.answer()

    if query.data == "why_club":
        # Показываем преимущества клуба
        await query.edit_message_text(text=BENEFITS_TEXT, parse_mode="Markdown")
        # Возвращаем кнопку "Назад"
        keyboard = [[InlineKeyboardButton("Назад", callback_data="back_to_main")]]
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return START

    elif query.data == "join_club":
        # Вторая менюшка с вариантами оплаты
        keyboard = [
            [
                InlineKeyboardButton("Оплатить картой РФ", callback_data="pay_ru"),
                InlineKeyboardButton(
                    "Оплатить зарубежной картой", callback_data="pay_foreign"
                ),
            ],
            [InlineKeyboardButton("Назад", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        payment_text = """
💳 *Выберите способ оплаты:*

🇷🇺 *Картой РФ*:
   - Сбербанк, Тинькофф, Альфа-Банк
   - Мгновенное зачисление
   - Стоимость: 1499₽/месяц

🌍 *Зарубежной картой*:
   - Visa, Mastercard, American Express
   - Конвертация по курсу ЦБ
   - Стоимость: $15/месяц
   
🎓 *После оплаты вы получите*:
   - Доступ к закрытому чату клуба
   - Персональный план обучения
   - Приветственный пакет материалов
        """

        await query.edit_message_text(
            text=payment_text, reply_markup=reply_markup, parse_mode="Markdown"
        )
        return JOIN_CLUB

    elif query.data == "back_to_main":
        # Возвращаемся в главное меню
        keyboard = [
            [
                InlineKeyboardButton("Вступить в клуб", callback_data="join_club"),
                InlineKeyboardButton("Зачем тебе в клуб", callback_data="why_club"),
            ],
            [
                InlineKeyboardButton("Поддержка", url="https://t.me/+lnXg7LoeBgg2MzY6"),
                InlineKeyboardButton("Отзывы", url="https://t.me/+IOifOfhVPnw4MTEy"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=CLUB_DESCRIPTION, reply_markup=reply_markup, parse_mode="Markdown"
        )
        return START

    elif query.data in ["pay_ru", "pay_foreign"]:
        # Обработка выбора оплаты
        if query.data == "pay_ru":
            payment_info = """
✅ *Оплата картой РФ*

Для оплаты перейдите по ссылке:
https://t.me/english_payment_bot?start=ru_payment

Или используйте реквизиты:
• Счет: 2200 1234 5678 9012
• БИК: 044525225
• Назначение: "English Club"

После оплаты нажмите "Проверить оплату"
            """
        else:  # pay_foreign
            payment_info = """
✅ *Оплата зарубежной картой*

Для оплаты перейдите по ссылке:
https://buy.stripe.com/test_123456789

Доступные карты:
• Visa
• Mastercard
• American Express

Сумма: $15.00 USD

После оплаты нажмите "Проверить оплату"
            """

        keyboard = [
            [InlineKeyboardButton("Проверить оплату", callback_data="check_payment")],
            [InlineKeyboardButton("Назад к оплате", callback_data="join_club")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=payment_info, reply_markup=reply_markup, parse_mode="Markdown"
        )
        return PAYMENT

    elif query.data == "check_payment":
        # Имитация проверки оплаты
        await query.edit_message_text(
            text="⏳ *Проверяем оплату...*\n\n"
            "Обычно это занимает 1-2 минуты. Как только оплата будет подтверждена, "
            "вы получите доступ ко всем материалам клуба!",
            parse_mode="Markdown",
        )

        # Имитация задержки проверки оплаты
        import asyncio

        await asyncio.sleep(2)

        # Сообщение об успехе
        await query.edit_message_text(
            text="🎉 *Поздравляем!* Оплата подтверждена!\n\n"
            "Теперь вы полноправный член English Club!\n\n"
            "*Ваши следующие шаги:*\n"
            "1. Присоединяйтесь к чату: https://t.me/english_club_chat\n"
            "2. Пройдите тест на уровень: /test\n"
            "3. Запишитесь на первое занятие: /schedule\n\n"
            "Добро пожаловать в клуб! 🚀",
            parse_mode="Markdown",
        )
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение диалога"""
    await update.message.reply_text(
        "Диалог завершен. Для начала нажмите /start", reply_markup=None
    )
    return ConversationHandler.END


async def start_WebApp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton(
                "Открыть веб-приложение",
                web_app=WebAppInfo(url=WEBHOOK_URL + WEBAPP_PATH),
            )
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здесь будет запускться вебэп.",
        reply_markup=markup,
    )
