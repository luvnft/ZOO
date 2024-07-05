from fastapi import APIRouter, Request
import json

from zootopia.config.config import config
from zootopia.context.context import ZootopiaContext
from zootopia.brain.brain import DigitalBrain
from zootopia.utils.logger import logger

router = APIRouter()


@router.post("/message")
async def message_webhook(request: Request):
    try: 
        request_body = json.loads(await request.body())
        context = ZootopiaContext(request_body, config)
        logger.info(f"Received {context.message.provider.value}) message: "
            f"{context.message}"
        )
        zootopian = DigitalBrain(context)
        await zootopian.detect_intent()
    except Exception as e:
        logger.info("Error")
    
    return {"message": "Received"}