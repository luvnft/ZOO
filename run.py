import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.config.config import config
from src.messaging.telegrambot import TelegramBot
from src.routers.gauth import router as gauth_router
from src.routers.message import router as message_router
from src.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Request: {request.method} {request.url}")
        print(f"From: {request.client.host}")
        print(f"Headers: {request.headers}")
        body = await request.body()
        print(f"Body: {body.decode()}")
        response = await call_next(request)
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before start
    logger.info("Starting application.")

    if os.getenv("USE_NGROK") == "true":
        from pyngrok import ngrok

        ngrok_connection = ngrok.connect(addr="127.0.0.1:8000", proto="http")
        print(ngrok_connection.public_url)

        _bot = TelegramBot.from_config(config.MESSAGING_CONFIG.TELEGRAM)
        asyncio.get_event_loop().create_task(
            _bot.register_webhook(f"{ngrok_connection.public_url}/telegram")
        )
    else:
        _bot = TelegramBot.from_config(config.MESSAGING_CONFIG.TELEGRAM)
        asyncio.get_event_loop().create_task(
            _bot.register_webhook("https://ai-assistant-0qu9.onrender.com/telegram")
        )

    yield

    # after close
    logger.info("Closing application.")
    if os.getenv("USE_NGROK") == "true":
        ngrok.disconnect(ngrok_connection.public_url)
        ngrok.kill()


# Loading FastAPI app
app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.include_router(message_router)
app.include_router(gauth_router)
