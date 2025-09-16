from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import json
import os

# 🔑 Токен твоего бота
BOT_TOKEN = "8126131226:AAH52Ad8CwWfuPIdH0YnRNPhGVwsUucpAFY"

# 🌐 URL твоего магазина на Render (БЕЗ ПРОБЕЛОВ!)
WEB_APP_URL = "https://dorlowpegas.onrender.com"

# 📩 ID администратора (теперь правильно!)
ADMIN_ID = 494863358

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Команда /start — отправляем кнопку Web App
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Открыть магазин 🛒", web_app=web_app))
    await message.answer(
        "🍓 Добро пожаловать в наш магазин десертов!\n\n"
        "Выбирайте товары, добавляйте в корзину и оформляйте заказ — всё прямо здесь, в Telegram!",
        reply_markup=keyboard
    )

# Обработка данных из Web App (после оформления заказа)
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    data = message.web_app_data.data  # JSON-строка с данными формы
    user = message.from_user

    # 💾 Сохраняем заказ в файл orders.json
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
    await message.answer("✅ Ваш заказ успешно оформлен! Мы свяжемся с вами в ближайшее время для уточнения деталей.")

    # 📩 Отправляем заказ админу
    try:
        await bot.send_message(
            ADMIN_ID,
            f"📦 *Новый заказ!*\n\n"
            f"👤 Пользователь: @{user.username or 'не указан'} ({user.first_name})\n"
            f"🆔 ID: {user.id}\n"
            f"📋 Данные: {data}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print("Не удалось отправить сообщение админу:", e)

# Запуск бота
if __name__ == '__main__':
    print("🚀 Бот запущен и готов принимать заказы!")
    executor.start_polling(dp, skip_updates=True)
