from fastapi import APIRouter, Request
from src.config.config import config
from src.manager.manager import Manager
from src.utils.logger import logger
from src.messaging.factory import MessagingProviderFactory
from src.messaging.models import Message

router = APIRouter()


@router.post("/message")
async def message_webhook(request: Request):
    try: 
        messaging_service, request_body = await MessagingProviderFactory.create_provider(request, config=config.MESSAGING_CONFIG)
        message: Message = await messaging_service.receive_message(request_body)

        logger.info(  # pylint: disable=W1203
            f"Received Message (from {message.medium.value}): "
            f"{message}"
        )

        manager = Manager(messaging_service, message)
        intent = await manager.find_intent()
        logger.info(intent)
    except Exception as e:
        logger.error("Unexpected error when recieving message: %s", e)
        intent = await manager.simple_response()
        logger.info(intent)
        return {"message": "Received"}

    return {"message": "Received"}

