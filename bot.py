import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties

# 🔐 Токен бота
TOKEN = "8093577977:AAFpJGqDIGSWIWi21zP3SUAdVEiZ8-wOaCg"

# 👤 ID администратора
ADMIN_ID = 6270030591

# 🔧 Инициализация
from aiogram import Router

router = Router()
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# 🧠 Подключаем роутеры
dp.include_router(router)

# 📦 Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Прайс")],
        [KeyboardButton(text="📦 Наличие на складе")],
        [KeyboardButton(text="📝 Сделать заказ")],
        [KeyboardButton(text="❓ FAQ")],
        [KeyboardButton(text="📢 Подписаться на рассылку")]
    ],
    resize_keyboard=True
)

# 🧾 Обработчик /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Выбери команду:", reply_markup=main_keyboard)

# 📋 Прайс-лист
price_list = """
<b>Прайс-лист:</b>
...
"""

# 📄 Обработчик "📋 Прайс"
@router.message(F.text == "📋 Прайс")
async def handle_price(message: Message):
    await message.answer(price_list)
    try:
        file = FSInputFile("price.pdf")
        await message.answer_document(file, caption="📄 Прайс в PDF формате")
    except FileNotFoundError:
        await message.answer("❌ PDF-файл прайса не найден.")

# 📦 Обработчик "Наличие на складе"
@router.message(F.text == "📦 Наличие на складе")
async def stock_handler(message: Message):
    try:
        with open("stock.txt", "r", encoding="utf-8") as f:
            stock = f.read()
        await message.answer(f"<b>📦 В наличии:</b>\n{stock}")
    except FileNotFoundError:
        await message.answer("❌ Не удалось загрузить данные о наличии товаров.")

# 📝 Обработчик "Сделать заказ"
@router.message(F.text == "📝 Сделать заказ")
async def order_handler(message: Message):
    await message.answer("✍️ Напишите, пожалуйста, какие товары вы хотите заказать. Укажите количество и контакт для связи.")

# 📬 Отправка заказа админу
@router.message(F.text & ~F.text.in_(["📋 Прайс", "📦 Наличие на складе", "📝 Сделать заказ", "❓ FAQ", "📢 Подписаться на рассылку"]))
async def handle_order_text(message: Message):
    if message.reply_to_message and "заказать" in message.reply_to_message.text.lower():
        return
    text = f"📥 Новый заказ от @{message.from_user.username or 'пользователь'}:\n\n{message.text}"
    await bot.send_message(chat_id=ADMIN_ID, text=text)
    await message.answer("✅ Спасибо за заказ! Мы скоро свяжемся с вами.")

# ❓ FAQ
@router.message(F.text == "❓ FAQ")
async def faq_handler(message: Message):
    faq = (
        "❓ <b>Часто задаваемые вопросы:</b>\n\n"
        "1. <b>Как оплатить?</b>\n— Переводом на карту/Выставления счёта на ЮР лицо(клинику).\n\n"
        "2. <b>Как происходит доставка?</b>\n— Через СДЭК или Boxberry.\n\n"
        "3. <b>Есть ли гарантия?</b>\n— Да, на все товары действует официальная гарантия.\n\n"
        "4. <b>Как получить консультацию?</b>\n— Напишите ваш вопрос — мы ответим лично."
    )
    await message.answer(faq)

# 📢 Подписка на рассылку
@router.message(F.text == "📢 Подписаться на рассылку")
async def subscribe_handler(message: Message):
    await message.answer("✅ Вы подписаны на рассылку. Новости и акции будут приходить сюда!")

# 🚀 Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# 🌐 Минимальный FastAPI сервер для Render
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "Bot is running"}

def run_server():
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    import os
    from threading import Thread

    # Запускаем FastAPI сервер в отдельном потоке
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Запускаем Telegram-бота с защитой от крашей
    asyncio.run(main())


