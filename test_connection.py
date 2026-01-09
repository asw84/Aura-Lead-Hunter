"""
Простой тест подключения к Telegram API.
"""

import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# Твои credentials
API_ID = 29772885
API_HASH = "36062a53da786099926a4f663cfb6134"
PHONE = "+79862206823"

async def test_connection():
    print("🔌 Подключение к Telegram...")
    
    client = TelegramClient(
        "sessions/test_session",
        API_ID,
        API_HASH
    )
    
    try:
        await client.connect()
        print("✅ Подключение к Telegram успешно!")
        
        # Проверяем авторизацию
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Уже авторизован как @{me.username}")
        else:
            print("📱 Требуется авторизация...")
            print(f"📞 Отправляю запрос кода на {PHONE}...")
            
            try:
                result = await client.send_code_request(PHONE)
                print(f"✅ Код отправлен!")
                print(f"   Тип отправки: {result.type.__class__.__name__}")
                print(f"   Phone code hash: {result.phone_code_hash[:10]}...")
                
                code = input("\n▶️ Введите код: ").strip()
                await client.sign_in(PHONE, code)
                me = await client.get_me()
                print(f"✅ Авторизация успешна! Привет, @{me.username}!")
                
            except FloodWaitError as e:
                print(f"⚠️ FloodWait: нужно подождать {e.seconds} секунд")
                print(f"   Это значит код уже был отправлен ранее.")
                print(f"   Проверь Telegram на телефоне!")
                
    except Exception as e:
        print(f"❌ Ошибка: {type(e).__name__}: {e}")
    
    finally:
        await client.disconnect()
        print("\n🔌 Отключено")

if __name__ == "__main__":
    asyncio.run(test_connection())
