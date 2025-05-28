import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties

# 🔐 Твой токен
TOKEN = "8093577977:AAFpJGqDIGSWIWi21zP3SUAdVEiZ8-wOaCg"

# 👤 ID администратора
ADMIN_ID = 6270030591

# 🧠 Инициализация
router = Router()
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

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

# /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Выбери команду:", reply_markup=main_keyboard)

# 📋 Пример команды "Прайс"
@router.message(F.text == "📋 Прайс")
async def handle_price(message: Message):
    price_list = """
<b>Прайс-лист:</b>

1. ФАЙЛЫ S FLEXI — 2 100₽
2. ФАЙЛЫ R SHAPER — 1 700₽
"""
    await message.answer(price_list)

# ▶️ Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())