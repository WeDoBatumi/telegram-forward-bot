import os
from telethon import TelegramClient, events
from aiohttp import web
import asyncio

# 🔐 Данные авторизации
api_id = 28262196
api_hash = '3312838d662c74183e9adacb005bb2fc'
session_name = 'my_main_account'

# 🔑 Ключевые слова
keywords = ['ноут', 'ноутбук', 'мак', 'мак бук', 'макбук', 'mac', 'mac book', 'macbook']
# 🚫 Исключения
stop_words = ['работа', 'работы', 'apple macbook', 'ipad']

# 📬 Куда пересылать
target_user = 'WeDo_Batumi'

# 🌐 Порт Render
PORT = int(os.environ.get('PORT', 8000))

client = TelegramClient(session_name, api_id, api_hash)

# 🌍 Web-сервер для Render
app = web.Application()
app.router.add_get('/', lambda request: web.Response(text="Bot is running"))

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"✅ Web-сервер на порту {PORT}")

@client.on(events.NewMessage(chats=None))
async def handler(event):
    message_text = event.message.message or ""
    sender = await event.get_sender()

    # Стоп-слова
    if any(word in message_text.lower() for word in stop_words):
        print("⛔️ Найдено стоп-слово, сообщение проигнорировано.")
        return

    # Ключевые слова
    if any(word in message_text.lower() for word in keywords):
        try:
            # Получить ссылку
            try:
                link = await event.message.get_permalink()
            except:
                link = None

            # Название или username чата
            chat_title = getattr(event.chat, 'title', None)
            chat_username = getattr(event.chat, 'username', None)

            source_name = f"💬 {chat_title}" if chat_title else f"👤 @{chat_username}" if chat_username else "🔹 Неизвестный источник"
            message_link = f"🔗 {link}" if link else "⚠️ Ссылка недоступна"

            text_to_send = f"{source_name}\n\n{message_text.strip()}\n\n{message_link}"

            await client.send_message(target_user, text_to_send)
            print("✅ Переслано:", source_name)

        except Exception as e:
            print("❌ Ошибка пересылки:", e)

# 🚀 Запуск
async def main():
    print("🚀 Бот запущен и слушает сообщения.")
    await start_web()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
