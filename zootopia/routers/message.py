from fastapi import APIRouter, Request
from zootopia.config.config import config
from zootopia.manager.manager import Manager
from zootopia.utils.logger import logger
from zootopia.app_state.app_state import ZootopiaAppState
import json

router = APIRouter()


@router.post("/message")
async def message_webhook(request: Request):
    # try: 
        request_body = json.loads(await request.body())
        app_state = ZootopiaAppState(request_body, config)
        logger.info(  # pylint: disable=W1203
            f"Received Message (from {app_state.message.provider.value}): "
            f"{app_state.message}"
        )
        manager = Manager(app_state)
        intent = await manager.find_intent()
        logger.info(intent)

    # except Exception as e:
    #     logger.error("Unexpected error when recieving message: %s", e)
    #     intent = await manager.simple_response()
    #     logger.info(intent)
    #     return {"message": "Received"}

        return {"message": "Received"}

