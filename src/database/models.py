from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Union, Dict, Type
from pydantic import BaseModel, Field


class SupabaseConfig(BaseModel):
    URL: str
    KEY: str


class _TableIDConfig(BaseModel):
    USER: str
    GAUTH: str
    MESSAGE: str


class _UserIDConfig(BaseModel):
    TELEGRAM: str
    EMAIL: str


class ConstantIDConfig(BaseModel):
    TABLE_IDS: _TableIDConfig
    USER_IDS: _UserIDConfig
    ID_COLUMN_NAME: str

class GAuthTable(BaseModel):
    access_token: str
    refresh_token: str
    token_expiry: Optional[str] = None
    token_uri: str
    user_agent: Optional[str] = None

# class UserTable(BaseModel):
#     username: Optional[str] = None
#     telegram_id: Optional[int] = None
#     email_id: Optional[str] = None

class Tables(Enum):
    """Tables available in the database."""
    AGENTS = "agents"
    AGENTS__id = "id"
    AGENTS__role = "role"
    AGENTS__first_message = "first_message"

    USERS = "users"
    USERS__id = "id"
    USERS__created_at = "created_at"
    USERS__phone_number = "phone_number"
    USERS__birthday = "birthday"

    ROOMS = "rooms"
    ROOMS__id = "id"
    ROOMS__created_at = "created_at"
    ROOMS__user_id = "user_id"
    ROOMS__agent_id = "agent_id"
    ROOMS__bird_channel_id = "bird_channel_id"
    ROOMS__telegram_chat_id = "telegram_chat_id"

    MESSAGES = "messages"
    MESSAGES__id = "id"
    MESSAGES__room_id = "room_id"
    MESSAGES__session_id = "session_id"
    MESSAGES__created_at = "created_at"
    MESSAGES__from_user = "from_user"
    MESSAGES__message = "message"

def utc_now():
    return datetime.now(timezone.utc)

class AgentModel(BaseModel):
    id: Optional[int] = None
    role: str
    first_message: str

class UserModel(BaseModel):
    id: Optional[int] = None
    created_at: datetime = Field(default_factory=utc_now)
    phone_number: Optional[str]
    birthday: Optional[datetime]

class RoomModel(BaseModel):
    id: Optional[int] = None
    created_at: datetime = Field(default_factory=utc_now)
    user_id: int
    agent_id: int
    bird_channel_id: Optional[str]
    telegram_chat_id: Optional[str]

class MessageModel(BaseModel):
    id: Optional[int] = None
    room_id: int
    created_at: datetime = Field(default_factory=utc_now)
    from_user: bool
    message: str

TableModel = Union[UserModel, AgentModel, MessageModel, RoomModel]

TABLE_MODEL_MAP: Dict[str, Type[TableModel]] = {
    "users": UserModel,
    "rooms": RoomModel,
    "agents": AgentModel,
    "messages": MessageModel,
}

