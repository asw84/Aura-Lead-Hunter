"""
Aura Lead Hunter - Telegram Client
====================================
Modular Telethon client for UserBot operations.
Handles session management and connection lifecycle.
"""

import asyncio
from pathlib import Path
from typing import Optional, List, Union
from dataclasses import dataclass

from telethon import TelegramClient as TelethonClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    FloodWaitError,
    AuthKeyUnregisteredError
)
from telethon.tl.types import User, Channel, Chat

from config.settings import TelegramConfig
from utils.logger import AuraLogger, ThoughtType


@dataclass
class ConnectionState:
    """Tracks client connection state."""
    is_connected: bool = False
    is_authorized: bool = False
    user_id: Optional[int] = None
    username: Optional[str] = None


class TelegramClientWrapper:
    """
    Modular wrapper around Telethon client.
    Handles session management, connection, and authentication.
    """
    
    def __init__(
        self,
        config: TelegramConfig,
        logger: Optional[AuraLogger] = None
    ):
        self.config = config
        self.logger = logger
        self.state = ConnectionState()
        
        # Ensure sessions directory exists
        Path("sessions").mkdir(parents=True, exist_ok=True)
        
        # Initialize Telethon client
        session_path = str(self.config.session_path)
        self._client = TelethonClient(
            session_path,
            self.config.api_id,
            self.config.api_hash,
            device_model="Aura Lead Hunter",
            system_version="1.0",
            app_version="1.0.0",
            lang_code="en"
        )
        
        self._log(ThoughtType.SYSTEM, "Client initialized", {
            "session": session_path,
            "api_id": str(self.config.api_id)[:4] + "***"
        })
    
    def _log(self, thought_type: ThoughtType, action: str, details: dict = None) -> None:
        """Log client action."""
        if self.logger:
            self.logger.thought(thought_type, "TelegramClient", action, details)
    
    @property
    def client(self) -> TelethonClient:
        """Get the underlying Telethon client."""
        return self._client
    
    async def connect(self) -> bool:
        """
        Connect to Telegram.
        Returns True if connected and authorized.
        """
        try:
            self._log(ThoughtType.CONNECT, "Connecting to Telegram...")
            
            await self._client.connect()
            self.state.is_connected = True
            
            # Check if already authorized
            if await self._client.is_user_authorized():
                me = await self._client.get_me()
                self.state.is_authorized = True
                self.state.user_id = me.id
                self.state.username = me.username
                
                self._log(ThoughtType.SUCCESS, "Connected and authorized", {
                    "user_id": self.state.user_id,
                    "username": f"@{self.state.username}"
                })
                return True
            
            # Need to authorize
            self._log(ThoughtType.CONNECT, "Session not authorized, starting auth flow")
            return await self._authorize()
            
        except AuthKeyUnregisteredError:
            self._log(ThoughtType.ERROR, "Session expired or invalid, need to re-auth")
            # Delete old session and retry
            session_file = Path(f"{self.config.session_path}.session")
            if session_file.exists():
                session_file.unlink()
            return await self.connect()
            
        except Exception as e:
            self._log(ThoughtType.ERROR, f"Connection failed: {e}")
            raise
    
    async def _authorize(self) -> bool:
        """
        Handle authorization flow.
        Sends code to phone and waits for user input.
        """
        try:
            self._log(ThoughtType.CONNECT, "Sending code request", {
                "phone": self.config.phone[:4] + "***"
            })
            
            try:
                sent_code = await self._client.send_code_request(self.config.phone)
                self._log(ThoughtType.CONNECT, f"Code sent via {sent_code.type.__class__.__name__}")
            except FloodWaitError as e:
                print(f"\n⚠️ Telegram требует подождать {e.seconds} секунд перед повторной отправкой кода.")
                print(f"⏳ Ожидание {e.seconds}s...")
                self._log(ThoughtType.WARNING, f"FloodWait on code request: {e.seconds}s")
                import asyncio
                await asyncio.sleep(e.seconds + 5)
                sent_code = await self._client.send_code_request(self.config.phone)
            
            # Wait for code input
            print("\n" + "="*60)
            print("📱 ТЕЛЕГРАМ АВТОРИЗАЦИЯ")
            print("="*60)
            print(f"📲 Код отправлен на номер: {self.config.phone}")
            print("")
            print("🔍 ГДЕ ИСКАТЬ КОД:")
            print("   1. В приложении Telegram - сообщение от 'Telegram'")
            print("   2. В 'Избранное' (Saved Messages)")
            print("   3. Как push-уведомление на телефоне")
            print("   4. Редко - по SMS")
            print("="*60)
            code = input("▶️ Введите 5-значный код: ").strip()
            
            try:
                await self._client.sign_in(self.config.phone, code)
            except SessionPasswordNeededError:
                # 2FA enabled
                print("\n🔐 Требуется двухфакторная аутентификация")
                password = input("Введите пароль 2FA: ")
                await self._client.sign_in(password=password)
            
            me = await self._client.get_me()
            self.state.is_authorized = True
            self.state.user_id = me.id
            self.state.username = me.username
            
            self._log(ThoughtType.SUCCESS, "Authorization successful", {
                "user_id": self.state.user_id,
                "username": f"@{self.state.username}"
            })
            
            print(f"\n✅ Авторизация успешна! Привет, @{self.state.username}!")
            
            return True
            
        except PhoneCodeInvalidError:
            self._log(ThoughtType.ERROR, "Invalid code entered")
            print("\n❌ Неверный код! Попробуйте ещё раз.")
            return False
        except FloodWaitError as e:
            self._log(ThoughtType.ERROR, f"Flood wait: {e.seconds}s")
            print(f"\n❌ Telegram заблокировал запросы на {e.seconds}s. Подождите и попробуйте снова.")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self.state.is_connected:
            await self._client.disconnect()
            self.state.is_connected = False
            self.state.is_authorized = False
            self._log(ThoughtType.SYSTEM, "Disconnected")
    
    async def get_entity(self, entity: Union[str, int]) -> Optional[Union[User, Channel, Chat]]:
        """
        Get entity (user, channel, or chat) by username or ID.
        """
        try:
            return await self._client.get_entity(entity)
        except Exception as e:
            self._log(ThoughtType.WARNING, f"Failed to get entity: {entity}", {"error": str(e)})
            return None
    
    async def join_chat(self, chat_link: str) -> Optional[Union[Channel, Chat]]:
        """
        Join a chat/channel by username or invite link.
        Returns the chat entity if successful.
        """
        try:
            self._log(ThoughtType.JOIN_CHAT, f"Attempting to join: {chat_link}")
            
            # Handle invite links
            if "joinchat" in chat_link or "+" in chat_link:
                from telethon.tl.functions.messages import ImportChatInviteRequest
                
                # Extract hash from invite link
                invite_hash = chat_link.split("/")[-1].replace("+", "")
                result = await self._client(ImportChatInviteRequest(invite_hash))
                chat = result.chats[0] if result.chats else None
            else:
                # Regular username/channel
                chat = await self._client.get_entity(chat_link)
                
                # Check if we need to join
                if hasattr(chat, 'left') and chat.left:
                    from telethon.tl.functions.channels import JoinChannelRequest
                    await self._client(JoinChannelRequest(chat))
            
            if chat:
                chat_title = getattr(chat, 'title', str(chat.id))
                self._log(ThoughtType.SUCCESS, f"Joined chat: {chat_title}", {
                    "chat_id": chat.id,
                    "title": chat_title
                })
            
            return chat
            
        except FloodWaitError as e:
            self._log(ThoughtType.ERROR, f"Flood wait on join: {e.seconds}s")
            raise
        except Exception as e:
            self._log(ThoughtType.ERROR, f"Failed to join {chat_link}: {e}")
            return None
    
    async def get_dialogs(self, limit: int = 100) -> List:
        """Get list of dialogs (chats)."""
        return await self._client.get_dialogs(limit=limit)
    
    async def iter_messages(
        self,
        chat: Union[str, int, Channel, Chat],
        limit: int = 100,
        **kwargs
    ):
        """
        Iterate over messages in a chat.
        This is a generator that yields messages.
        """
        async for message in self._client.iter_messages(chat, limit=limit, **kwargs):
            yield message
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


# Alias for backward compatibility
TelegramClient = TelegramClientWrapper
