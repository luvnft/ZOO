from abc import ABC, abstractmethod
from typing import Optional

from fastapi import Request

from src.messaging.models import Message


class BaseMessaging(ABC):
    @classmethod
    @abstractmethod
    def from_config(cls, config):
        """Instantiate and return a messaging object from configuration."""
        pass

    @classmethod
    @abstractmethod
    async def receive_message(cls, request: Request) -> Message:
        """Handle an incoming message from a sender."""
        pass

    @abstractmethod
    async def send_message(self, message: str, user_id: int) -> Optional[str]:
        """Send a message to a recipient."""
        pass

    @abstractmethod
    async def register_webhook(self, webhook_url: str) -> bool:
        """Register a webhook URL for receiving updates."""
        pass
