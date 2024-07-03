from typing import Union, Tuple
from fastapi import Request
import json
from zootopia.utils.logger import logger
from .basemessaging import BaseMessaging
from .bird import BirdSMSProvider
from .telegrambot import TelegramBot
from zootopia.config.config import MessagingConfig
from .models import (
    MessageParsingError,
)

class MessagingProviderFactory:
    @staticmethod
    async def create_provider(request: Request, config: MessagingConfig) -> Tuple[BaseMessaging, dict]:
        request_body = json.loads(await request.body())

        if "payload" in request_body:  # Bird message
            logger.info("Bird message received")
            return BirdSMSProvider.from_config(config.BIRD), request_body

        elif "update_id" in request_body:  # Telegram message
            logger.info("Telegram message received")
            return TelegramBot.from_config(config.TELEGRAM), request_body

        else:
            raise MessageParsingError("Unknown message format")