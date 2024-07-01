from fastapi import APIRouter, Request

from src.config.config import config
from src.manager.manager import Manager
from src.messaging.telegrambot import TelegramBot
from src.utils.logger import logger
from src.messaging.factory import MessagingProviderFactory

router = APIRouter()


@router.post("/message")
async def message_webhook(request: Request):
    messaging_service, request_body = await MessagingProviderFactory.create_provider(request, config=config.MESSAGING_CONFIG)

    try: 
        received_message = await messaging_service.receive_message(request_body)
        received_uid = received_message.uid
        logger.info(  # pylint: disable=W1203
            f"Received Message (from {received_message.medium.value}): "
            f"{received_message}"
        )

        manager = Manager(messaging_service, received_message, received_uid)
        intent = await manager.find_intent()
        logger.info(intent)
    except Exception as e:
        logger.error("Unexpected error when recieving message: %s", e)
        intent = await manager.simple_response()
        logger.info(intent)
        return {"message": "Received"}

    return {"message": "Received"}

