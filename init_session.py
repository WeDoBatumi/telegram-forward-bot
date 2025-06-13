from telethon import TelegramClient

api_id = 28262196
api_hash = '3312838d662c74183e9adacb005bb2fc'
session_name = 'my_main_account'  # не меняй, должно совпадать с кодом бота

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await client.start()
    print("✅ Сессия успешно создана!")

client.loop.run_until_complete(main())