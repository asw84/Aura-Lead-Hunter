"""
Авторизация через QR-код (альтернативный метод).
Откроется QR-код в браузере - отсканируй через Telegram.
"""

import asyncio
import qrcode
from io import BytesIO
from telethon import TelegramClient
from telethon.tl.functions.auth import ExportLoginTokenRequest, ImportLoginTokenRequest
import base64
import webbrowser
import tempfile
import os

API_ID = 29772885
API_HASH = "36062a53da786099926a4f663cfb6134"

async def login_with_qr():
    print("🔌 Подключение к Telegram...")
    
    client = TelegramClient(
        "sessions/aura_lead_hunter",
        API_ID,
        API_HASH
    )
    
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Уже авторизован как @{me.username}")
        await client.disconnect()
        return
    
    print("\n📱 Авторизация через QR-код...")
    print("=" * 50)
    print("1. Открой Telegram на телефоне")
    print("2. Настройки → Устройства → Привязать устройство")
    print("3. Отсканируй QR-код")
    print("=" * 50)
    
    # Генерируем QR токен
    qr_login = await client.qr_login()
    
    print(f"\n🔗 URL для QR: {qr_login.url}")
    
    # Создаём QR-код
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_login.url)
    qr.make(fit=True)
    
    # Сохраняем как HTML и открываем
    img = qr.make_image(fill_color="black", back_color="white")
    
    temp_file = os.path.join(tempfile.gettempdir(), "telegram_qr.png")
    img.save(temp_file)
    
    print(f"\n📷 QR-код сохранён: {temp_file}")
    print("   Открываю в просмотрщике...")
    
    os.startfile(temp_file)
    
    print("\n⏳ Ожидаю сканирования QR-кода...")
    
    try:
        # Ждём авторизации
        user = await qr_login.wait(timeout=120)
        print(f"\n✅ Авторизация успешна! Привет, @{user.username}!")
    except asyncio.TimeoutError:
        print("\n❌ Время ожидания истекло. Попробуй снова.")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(login_with_qr())
