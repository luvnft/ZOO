from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List
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
    AGENTS = "agents"
    USERS = "users"
    ROOMS = "rooms"
    SESSIONS = "sessions"
    MESSAGES = "messages"

def utc_now():
    return datetime.now(timezone.utc)

class AgentData(BaseModel):
    id: Optional[int] = None
    role: str
    first_message: str

class UserData(BaseModel):
    id: Optional[int] = None
    created_at: datetime = Field(default_factory=utc_now)
    phone_number: Optional[str]
    birthday: Optional[datetime]

class RoomData(BaseModel):
    id: Optional[int] = None
    created_at: datetime = Field(default_factory=utc_now)
    user_id: int
    agent_id: int
    bird_channel_id: Optional[str]
    telegram_chat_id: Optional[str]

class SessionData(BaseModel):
    id: Optional[int] = None
    room_id: int
    created_at: datetime = Field(default_factory=utc_now)
    ended_at: Optional[datetime] = None
    is_processed: bool = False
    topics: Optional[List[str]] = None
    summary: Optional[str] = None

class MessageData(BaseModel):
    id: Optional[int] = None
    room_id: int
    session_id: int
    created_at: datetime = Field(default_factory=utc_now)
    from_user: bool
    message: str
