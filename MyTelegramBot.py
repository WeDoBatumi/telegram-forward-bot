import os
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat, User
from aiohttp import web
import asyncio

# 🔐 Твои данные
api_id = 28262196
api_hash = '3312838d662c74183e9adacb005bb2fc'
session_name = 'my_main_account'

# 🔑 Ключевые слова
keywords = ['ноут', 'ноутбук', 'мак', 'мак бук', 'макбук', 'mac', 'mac book', 'macbook']

# 🚫 Слова-исключения
stop_words = ['работа', 'работы', 'apple macbook', 'ipad']

# 📬 Куда пересылать
target_user = 'WeDo_Batumi'  # без @

# 🌐 Порт для Render (или локально 8000)
PORT = int(os.environ.get('PORT', 8000))

# 🤖 Клиент Telethon
client = TelegramClient(session_name, api_id, api_hash)

# 🌍 Простой веб-сервер для Render
app = web.Application()
app.router.add_get('/', lambda request: web.Response(text="Bot is running"))

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"🌐 Web server started on port {PORT}")

# 📩 Обработка новых сообщений
@client.on(events.NewMessage(chats=None))  # слушаем все публичные чаты и группы
async def handler(event):
    message_text = event.message.message or ""

    # Проверка стоп-слов
    if any(stop_word.lower() in message_text.lower() for stop_word in stop_words):
        print("⛔️ Сообщение содержит стоп-слова, пропускаем")
        return

    # Проверка ключевых слов
    if not any(keyword.lower() in message_text.lower() for keyword in keywords):
        return  # нет ключевых слов — игнорируем

    try:
        # Пересылаем оригинальное сообщение
        await client.forward_messages(target_user, event.message)
        print("✅ Переслано сообщение")

        # Используем event.chat (не get_chat())
        chat = event.chat

        if isinstance(chat, Channel):
            if getattr(chat, "username", None):
                link = f"https://t.me/{chat.username}/{event.message.id}"
                await client.send_message(target_user, f"👉 {link}")
                print(f"🔗 Отправлена ссылка: {link}")
            else:
                print("⚠️ Канал или группа без username — ссылка невозможна")
        elif isinstance(chat, Chat):
            print("ℹ️ Сообщение из обычной группы — ссылки нет")
        elif isinstance(chat, User):
            print("ℹ️ Сообщение из личного чата — ссылки нет")
        else:
            print("⚠️ Неизвестный тип чата")

    except Exception as e:
        print(f"❌ Ошибка при обработке сообщения: {e}")

# 🚀 Запуск бота
async def main():
    print("🤖 Бот запущен. Ожидает новые сообщения...")
    await start_web()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
