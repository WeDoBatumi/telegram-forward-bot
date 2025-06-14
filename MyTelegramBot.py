import os
from telethon import TelegramClient, events
from aiohttp import web
import asyncio

# 🔐 Твои данные
api_id = 28262196
api_hash = '3312838d662c74183e9adacb005bb2fc'
session_name = 'my_main_account'

# 🔑 Ключевые слова
keywords = [
    'ноут', 'ноутбук', 'мак', 'мак бук', 'макбук',
    'mac', 'mac book', 'macbook'
]

# 🚫 Стоп-слова
stop_words = [
    'работа', 'работы', 'apple macbook', 'ipad'
]

# 📬 Куда пересылать
target_user = 'WeDo_Batumi'  # без @

# 🌐 Порт для Render
PORT = int(os.environ.get('PORT', 8000))

# 🤖 Инициализация Telethon-клиента
client = TelegramClient(session_name, api_id, api_hash)

# 🌍 Минимальный aiohttp веб-сервер для Render
app = web.Application()
app.router.add_get('/', lambda request: web.Response(text="✅ Bot is running"))

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"🌐 Web server running on port {PORT}")

# 📩 Обработка входящих сообщений
@client.on(events.NewMessage(chats=None))  # Слушаем всё
async def handler(event):
    message = event.message
    message_text = message.message or ""

    # 🔍 Проверка на стоп-слова
    if any(word in message_text.lower() for word in stop_words):
        print("⛔ Стоп-слово найдено, сообщение пропущено.")
        return

    # ✅ Проверка на ключевые слова
    if any(word in message_text.lower() for word in keywords):
        try:
            await client.forward_messages(target_user, message)
            print(f"✅ Переслано сообщение из: {event.chat.title or event.chat.username}")
        except Exception as e:
            print(f"⚠️ Ошибка при пересылке: {e}")

# 🚀 Старт основного цикла
async def main():
    print("🤖 Бот запущен. Ожидает новые сообщения...")
    await start_web()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
