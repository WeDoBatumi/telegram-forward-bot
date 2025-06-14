import os
from telethon import TelegramClient, events
from aiohttp import web
import asyncio

api_id = 28262196
api_hash = '3312838d662c74183e9adacb005bb2fc'
session_name = 'my_main_account'

keywords = [
    'ноут', 'ноутбук', 'мак', 'мак бук', 'макбук',
    'mac', 'mac book', 'macbook'
]

stop_words = [
    'работа', 'работы', 'apple macbook', 'ipad'
]

target_user = 'WeDo_Batumi'
PORT = int(os.environ.get('PORT', 8000))

client = TelegramClient(session_name, api_id, api_hash)

app = web.Application()
app.router.add_get('/', lambda request: web.Response(text="✅ Bot is running"))

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

@client.on(events.NewMessage(chats=None))
async def handler(event):
    message = event.message
    message_text = message.message or ""

    if any(w in message_text.lower() for w in stop_words):
        return

    if any(w in message_text.lower() for w in keywords):
        try:
            await client.forward_messages(target_user, message)

            link = await message.get_permalink()
            if link:
                await client.send_message(target_user, f"👉 {link}")
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")

async def main():
    await start_web()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
