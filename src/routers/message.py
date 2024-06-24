from fastapi import APIRouter, Request

from src.config.config import config
from src.manager.manager import Manager
from src.messaging.telegrambot import TelegramBot
from src.utils.logger import logger

router = APIRouter()


@router.post("/telegram")
async def message_webhook(request: Request):
    messaging_service = TelegramBot.from_config(config.MESSAGING_CONFIG.TELEGRAM)

    try:
        recieved_message = await messaging_service.recieve_message(request)
        recieved_uid = recieved_message.uid
        logger.info(  # pylint: disable=W1203
            f"Recieved Message (from {recieved_message.medium.value}): "
            f"{recieved_message}"
        )

        manager = Manager(messaging_service, recieved_message, recieved_uid)
        intent = await manager.find_intent()
        logger.info(intent)
    except Exception as e:
        logger.error("Unexpected error when recieving message: %s", e)
        intent = await manager.simple_response()
        logger.info(intent)
        return {"message": "Received"}

    return {"message": "Received"}
