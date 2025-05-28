import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.client.default import DefaultBotProperties

# 🔐 Токен бота
TOKEN = "8093577977:AAFpJGqDIGSWIWi21zP3SUAdVEiZ8-wOaCg"

# 👤 ID для получения заказов
ADMIN_ID = 6270030591

# 🔧 Инициализация
router = Router()
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# 🧾 Клавиатура
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

# 💰 Прайс-лист
price_list = """
<b>Прайс-лист:</b>
1. ФАЙЛЫ S FLEXI — 2 100₽
2. ФАЙЛЫ R SHAPER — 1 700₽
3. ФАЙЛЫ ENDOVIEW — 2 500₽
4. ФАЙЛЫ APEX MAX — 2 250₽
5. ФАЙЛЫ GOLD TAPER — 2 050₽
6. ФАЙЛЫ N TWO — 1 250₽
7. ФАЙЛЫ KID FILE — 1 200₽
8. ФАЙЛЫ REATREAT — 2 150₽
9. ФАЙЛЫ SAFE OPENER — 1 900₽
10. ФАЙЛЫ GLYDE MASTER — 1 900₽
11. ФАЙЛЫ РУЧНЫЕ Н и К — 190₽
12. Апекслокатор APEX03s — 19 300₽
13. Апекслокатор APICCOLO — 22 300₽
14. Мотор R1 VORTEX — 39 200₽
15. Эндоактиватор EASYDO — 17 400₽
16. Инжектор GUTTAFILL02 — 67 500₽
17. Термоплаггер GUTTAEST02 — 37 900₽
18. SSG PLUG 1-NiTi — 2 800₽
19. SSG PLUG 1/2 — 2 800₽
20. SSG PLUG 3/4 — 2 800₽
21. Лампа ALLADIN02 — 12 250₽
22. Линейка R1 PLUS — 5 300₽
23. Игла 23G — 3 800₽
24. Игла 25G — 3 800₽
"""

# /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Выбери команду:", reply_markup=main_keyboard)

# 📋 Прайс
@router.message(F.text == "📋 Прайс")
async def handle_price(message: Message):
    await message.answer(price_list)
    try:
        file = FSInputFile("price.pdf")
        await message.answer_document(file, caption="📄 Прайс в PDF формате")
    except FileNotFoundError:
        await message.answer("❌ PDF-файл прайса не найден.")

# 📦 Наличие на складе
@router.message(F.text == "📦 Наличие на складе")
async def stock_handler(message: Message):
    try:
        with open("stock.txt", "r", encoding="utf-8") as f:
            stock = f.read()
        await message.answer(f"<b>📦 В наличии:</b>\n{stock}")
    except FileNotFoundError:
        await message.answer("❌ Не удалось загрузить данные о наличии товаров.")

# 📝 Сделать заказ
@router.message(F.text == "📝 Сделать заказ")
async def order_handler(message: Message):
    await message.answer("✍️ Напишите, пожалуйста, какие товары вы хотите заказать. Укажите количество и контакт для связи.")

# 📬 Обработка текста как заказа
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
        "1. <b>Как оплатить?</b>\n— Переводом на карту.\n\n"
        "2. <b>Как происходит доставка?</b>\n— Через СДЭК или Boxberry.\n\n"
        "3. <b>Есть ли гарантия?</b>\n— Да, на все товары действует официальная гарантия.\n\n"
        "4. <b>Как получить консультацию?</b>\n— Напишите ваш вопрос — мы ответим лично."
    )
    await message.answer(faq)

# 📢 Подписаться на рассылку
@router.message(F.text == "📢 Подписаться на рассылку")
async def subscribe_handler(message: Message):
    await message.answer("✅ Вы подписаны на рассылку. Новости и акции будут приходить сюда!")

# ▶️ Запуск
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
import uvicorn
from fastapi import FastAPI

app = FastAPI()
@app.get("/")
async def root():
    return {"status": "Bot is running"}

if __name__ == "__main__":
    import threading
    # Запускаем FastAPI сервер в отдельном потоке
    server_thread = threading.Thread(
        target=uvicorn.run,
        kwargs={"app": app, "host": "0.0.0.0", "port": int(os.getenv("PORT", 10000))}
    )
    server_thread.daemon = True
    server_thread.start()

    # Запускаем бота
    asyncio.run(main())
