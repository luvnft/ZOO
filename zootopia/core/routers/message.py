from fastapi import APIRouter, Request
import json

from config.config import config
from zootopia.controller import AgentController, ContextManager
from zootopia.core.utils.logger import logger

router = APIRouter()


@router.post("/message")
async def message_webhook(request: Request):
    try: 
        request_body = json.loads(await request.body())
        context = ContextManager(request_body, config)
        logger.info(f"Received {context.message.provider.value}) message: "
            f"{context.message}"
        )
        zootopian = AgentController(context)
        await zootopian.handle_message()
    except Exception as e:
        logger.info("Error")
    
    return {"message": "Received"}