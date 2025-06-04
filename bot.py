from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === Настройки ===
TOKEN = "8093577977:AAFpJGqDIGSWIWi21zP3SUAdVEiZ8-wOaCg"  # ← замени на свой токен
MAIN_PRICE_FILE = "price.pdf"
SOHO_PRICE_FILE = "soho_price.pdf"
YOUR_TELEGRAM_ID = 6270030591  # ← замени на свой ID (узнай у @myidbot)

# === Клавиатура ===
keyboard = [
    [KeyboardButton("📁 Прайс GEOSOFT"), KeyboardButton("📦 Наличие на складе")],
    [KeyboardButton("🧾 Прайс SOCO/Расходники")],
    [KeyboardButton("🛒 Сделать заказ")],
    [KeyboardButton("❓ FAQ")],
    [KeyboardButton("📩 Подписка на рассылку")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Хранилище состояний пользователей
user_states = {}

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 Добро пожаловать в бот GOFFSHTEIN!\n\n"
        "Уважаемый клиент, делая заказы через этого бота — Вы экономите время и деньги.\n"
        "Выберите нужный раздел ниже 👇",
        reply_markup=reply_markup
    )
# === Обработка сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # --- Основной прайс (GEOSOFT) ---
    if text == "📁 прайс geosoft".lower():
        try:
            with open("price.txt", "r", encoding="utf-8") as txt_file:
                price_text = txt_file.read()
            await update.message.reply_text(price_text)
            with open(MAIN_PRICE_FILE, "rb") as file:
                await update.message.reply_document(document=file, filename="Прайс-GEOSOFT.pdf")
        except FileNotFoundError:
            await update.message.reply_text("❌ Файл 'price.txt' или 'price.pdf' не найден в папке.")

    # --- Прайс SOCO / Расходники ---
    elif text == "🧾 прайс soco/расходники".lower():
        soho_text = (
            "📎 Прайс на расходники и продукты SOCO:\n\n"
            
        )
        await update.message.reply_text(soho_text)
        try:
            with open(SOHO_PRICE_FILE, "rb") as file:
                await update.message.reply_document(document=file, filename="Прайс-SOCO.pdf")
        except FileNotFoundError:
            await update.message.reply_text("❌ Файл 'soho_price.pdf' не найден в папке.")

    # --- Сделать заказ ---
    elif text == "🛒 сделать заказ".lower():
        await update.message.reply_text("📞 Введите ваше имя, телефон и список товаров:")
        user_states[update.message.from_user.id] = "awaiting_order"

    # --- Получить заказ себе в личку ---
    elif update.message.from_user.id in user_states and user_states[update.message.from_user.id] == "awaiting_order":
        order_text = (
            f"📦 Новый заказ от пользователя {update.message.from_user.first_name} "
            f"(@{update.message.from_user.username or 'без юзернейма'})\n\n"
            f"Сообщение:\n{update.message.text}"
        )
        try:
            await context.bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=order_text)
            await update.message.reply_text("✅ Ваш заказ отправлен! Мы свяжемся с вами.")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при отправке заказа: {str(e)}")
        finally:
            del user_states[update.message.from_user.id]

    # --- Наличие на складе ---
    elif text == "📦 наличие на складе".lower():
        await update.message.reply_text("✅ Все товары в наличии. Уточните количество у менеджера.")

    # --- FAQ ---
    elif text == "❓ faq".lower():
        faq_text = (
            "❓ Как оформить заказ?\n"
            "Напишите нам список товаров и мы вышлем счет.\n\n"
            "🚚 Есть ли доставка?\n"
            "Да, возможна по РФ и странам СНГ.\n\n"
            "📄 Можно ли оплатить по безналу?\n"
            "Да, предоставляем полный пакет документов."
        )
        await update.message.reply_text(faq_text)

    # --- Подписка на рассылку ---
    elif text == "📩 подписка на рассылку".lower():
        await update.message.reply_text("🔔 Вы успешно подписались на обновления!")

    # --- Неизвестная команда ---
    else:
        await update.message.reply_text("❌ Неизвестная команда. Используйте меню ниже.", reply_markup=reply_markup)


# === Запуск бота ===
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Бот запущен...")
app.run_polling()