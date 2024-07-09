
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Type, Union

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