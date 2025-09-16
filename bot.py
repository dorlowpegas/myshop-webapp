from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
import json
import os

# 🔑 Токен твоего бота
BOT_TOKEN = "8126131226:AAH52Ad8CwWfuPIdH0YnRNPhGVwsUucpAFY"

# 🌐 URL твоего магазина на Render
WEB_APP_URL = "https://dorlowpegas.onrender.com"

# 📩 ID администратора
ADMIN_ID = 494863358

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Команда /start — отправляем кнопку Web App
@router.message(Command("start"))
async def send_welcome(message: Message):
    web_app = WebAppInfo(url=WEB_APP_URL)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть магазин 🛒", web_app=web_app)]
    ])
    await message.answer(
        f"🍓 {hbold('Добро пожаловать в наш магазин десертов!')}\n\n"
        "Выбирайте товары, добавляйте в корзину и оформляйте заказ — всё прямо здесь, в Telegram!",
        reply_markup=keyboard
    )

# Обработка данных из Web App
@router.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    data = message.web_app_data.data
    user = message.from_user

    # 💾 Сохраняем заказ
    if not os.path.exists('orders.json'):
        with open('orders.json', 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open('orders.json', 'r+', encoding='utf-8') as f:
        orders = json.load(f)
        orders.append({
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "data": data
        })
        f.seek(0)
        json.dump(orders, f, ensure_ascii=False, indent=2)

    # ✅ Отправляем подтверждение пользователю
    await message.answer("✅ Ваш заказ успешно оформлен! Мы свяжемся с вами в ближайшее время.")

    # 📩 Отправляем админу
    try:
        await bot.send_message(
            ADMIN_ID,
            f"📦 *Новый заказ!*\n\n"
            f"👤 Пользователь: @{user.username or 'не указан'} ({user.first_name})\n"
            f"🆔 ID: {user.id}\n"
            f"📋 Данные: {data}",
            parse_mode="Markdown"
        )
        print(f"✅ Заказ отправлен админу (ID: {ADMIN_ID})")
    except Exception as e:
        print(f"❌ Ошибка при отправке админу: {e}")

# Тестовая команда
@router.message(Command("test"))
async def test_admin_message(message: Message):
    try:
        await bot.send_message(ADMIN_ID, "✅ Тест: бот может писать админу!")
        await message.answer("Тестовое сообщение отправлено.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# Регистрация роутера
dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())