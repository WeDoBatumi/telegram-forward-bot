import telethon
print("Telethon version:", telethon.__version__)

import os
from telethon import TelegramClient, events
from aiohttp import web
import asyncio

# 🔐 Твои данные
api_id = 28262196
api_hash = '3312838d662c74183e9adacb005bb2fc'
session_name = 'my_main_account'

# 🔑 Ключевые слова
keywords = ['ноут', 'ноутбук', 'мак', 'мак бук', 'макбук', 'mac', 'mac book', 'macbook']

# 🚫 Слова-исключения (при их наличии сообщение НЕ пересылается)
stop_words = ['работа', 'работы', 'apple macbook', 'ipad']

# 📬 Куда пересылать
target_user = 'WeDo_Batumi'  # без @

# Получаем порт из переменной окружения Render (если нет — 8000)
PORT = int(os.environ.get('PORT', 8000))

client = TelegramClient(session_name, api_id, api_hash)

# Веб-сервер, чтобы Render видел открытый порт
app = web.Application()
app.router.add_get('/', lambda request: web.Response(text="Bot is running"))

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"Web server started on port {PORT}")

@client.on(events.NewMessage(chats=None))  # None — слушаем все чаты
async def handler(event):
    message_text = event.message.message or ""

    # Проверяем стоп-слова — если есть, выходим
    if any(stop_word.lower() in message_text.lower() for stop_word in stop_words):
        print("Сообщение содержит стоп-слова, пропускаем")
        return

    # Проверяем ключевые слова
    if any(keyword.lower() in message_text.lower() for keyword in keywords):
        try:
            await client.forward_messages(entity=target_user, messages=event.message)
            print(f"Переслано сообщение из: {event.chat.title or event.chat.username}")
        except Exception as e:
            print(f"Ошибка пересылки: {e}")

async def main():
    print("Бот запущен. Ожидает новые сообщения...")
    # Запускаем веб-сервер параллельно с клиентом
    await start_web()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
