from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class TelegramBotConfig(BaseModel):
    TELEGRAM_BOT_TOKEN: str


class _TelegramPhoto(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    width: int
    height: int


class _TelegramTextEntity(BaseModel):
    offset: int
    length: int
    type: str


class _TelegramSticker(BaseModel):
    width: int
    height: int
    emoji: str
    set_name: str
    is_animated: bool
    type: str
    thumbnail: _TelegramPhoto
    thumb: _TelegramPhoto
    file_id: str
    file_unique_id: str
    file_size: int


class _TelegramLocation(BaseModel):
    latitude: float
    longitude: float


class _TelegramDocument(BaseModel):
    file_name: str
    mime_type: str
    thumbnail: _TelegramPhoto
    thumb: _TelegramPhoto
    file_id: str
    file_unique_id: str
    file_size: int


class _TelegramVenue(BaseModel):
    location: _TelegramLocation
    title: str
    address: str
    foursquare_id: str
    foursquare_type: str


class _TelegramUser(BaseModel):
    id: int
    is_bot: bool
    first_name: str = None  # Optional last name
    last_name: str = None  # Optional last name
    language_code: str


class _TelegramChat(BaseModel):
    id: int
    first_name: str = None  # Optional last name
    last_name: str = None  # Optional last name
    type: str


class _TelegramMessageBase(BaseModel):
    message_id: int
    from_: _TelegramUser
    chat: _TelegramChat
    date: int


class _TelegramMessageText(_TelegramMessageBase):
    text: str
    entities: Optional[List[_TelegramTextEntity]] = None


class _TelegramMessagePhoto(_TelegramMessageBase):
    photo: Optional[List[_TelegramPhoto]]


class _TelegramMessageSticker(_TelegramMessageBase):
    sticker: _TelegramSticker


class _TelegramMessageLocation(_TelegramMessageBase):
    location: _TelegramLocation
    venue: _TelegramVenue


class _TelegramMessageDocument(_TelegramMessageBase):
    document: _TelegramDocument


class TelegramMessage(BaseModel):
    update_id: int
    message: Union[
        _TelegramMessageText,
        _TelegramMessagePhoto,
        _TelegramMessageSticker,
        _TelegramMessageLocation,
        _TelegramMessageDocument,
    ]


class MessageMedium(Enum):
    TELEGRAM = "telegram"


class MessageType(Enum):
    TEXT = "text"
    FILE = "file"


class Message(BaseModel):
    message: Union[TelegramMessage]
    uid: Union[int, str]
    user_name: Optional[str]
    medium: MessageMedium
    type: MessageType


class MessageParsingError(Exception):
    """Custom exception for errors during message parsing."""


class SendMessageError(Exception):
    """Custom exception for errors during sending messages."""


class WebhookError(Exception):
    """Custom exception for errors during webhook registration."""
