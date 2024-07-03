import os
from enum import Enum
from typing import cast

import yaml
from pydantic import BaseModel, ValidationError

from zootopia.autodb.models import AutoDBConfig
from zootopia.database.models import ConstantIDConfig, SupabaseConfig, _UserIDConfig
from zootopia.gsuite.models import GAuthConfig
from zootopia.messaging.models import TelegramBotConfig, BirdConfig

# There's gotta be a better way to do this (i used groq lol)


class CalendarConfig(BaseModel):
    CALENDAR_NAME: str
    CALENDAR_DESCRIPTION: str

class DriveConfig(BaseModel):
    FOLDER_NAME: str
    FILE_NAME_FORMAT: str

class GAuthConfig(BaseModel):
    GOOGLE_API_KEY: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_AUTH_SCOPE: list[str]
    CALENDAR: CalendarConfig
    DRIVE: DriveConfig

class WebAccessConfig(BaseModel):
    GOOGLE: GAuthConfig

class TelegramBotConfig(BaseModel):
    TELEGRAM_BOT_TOKEN: str

class BirdConfig(BaseModel):
    BIRD_API_URL: str
    BIRD_ORGANIZATION_ID: str
    BIRD_WORKSPACE_ID: str
    BIRD_API_KEY: str
    BIRD_SIGNING_KEY: str
    BIRD_CHANNEL_ID: str

class MessagingConfig(BaseModel):
    TELEGRAM: TelegramBotConfig
    BIRD: BirdConfig

class SupabaseConfig(BaseModel):
    URL: str
    KEY: str

class DatabaseConfig(BaseModel):
    SUPABASE: SupabaseConfig

class LLMConfig(BaseModel):
    GEMINI: dict[str, str]
    GROQ: dict[str, str]
    OPENAI: dict[str, str]
    ANTHROPIC: dict[str, str]

class IntentDetectionConfig(BaseModel):
    ENABLED: bool
    MODEL: str
    CONFIDENCE_THRESHOLD: float

class HumanLikeMemoryConfig(BaseModel):
    ENABLED: bool
    STORAGE: str
    MEMORY_LIFETIME: int
    IMPORTANCE_THRESHOLD: float

class InternetSearchConfig(BaseModel):
    ENABLED: bool
    API_KEY: str
    SAFE_SEARCH: bool
    RESULT_LIMIT: int

class CancelConfig(BaseModel):
    ENABLED: bool
    REDIS_URL: str

class BehaviorsConfig(BaseModel):
    INTENT_DETECTION: IntentDetectionConfig
    HUMAN_LIKE_MEMORY: HumanLikeMemoryConfig
    INTERNET_SEARCH: InternetSearchConfig
    CANCEL_CONFIG: CancelConfig

class ZootopiaConfig(BaseModel):
    MESSAGING_CONFIG: MessagingConfig
    DATABASE_CONFIG: DatabaseConfig
    WEB_ACCESS_CONFIG: WebAccessConfig
    LLM_CONFIG: LLMConfig
    BEHAVIORS_CONFIG: BehaviorsConfig


def set_environment_variables(config_data, prefix=""):
    """
    Set environment variables from the configuration data.
    """
    for key, value in config_data.items():
        env_key = f"{prefix}_{key}" if prefix else key
        if isinstance(value, dict):
            set_environment_variables(value, env_key)
        else:
            os.environ[env_key] = str(value)


def load_config(
    config_path: str, set_env: bool = False, config_type: type[ZootopiaConfig] = ZootopiaConfig
) -> BaseModel:
    """Loads configuration from a YAML file."""

    with open(config_path, "r", encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file)

    if set_env:
        set_environment_variables(config_data)

    try:
        return config_type(**config_data)
    except ValidationError as e:
        raise ValueError(f"Error parsing configuration: {e}") from e


testing = True
prefix = "zootopia/config/" if testing else "/etc/secrets/"
config = cast(ZootopiaConfig, load_config(f"{prefix}local.yaml", set_env=True))
autodb_config = cast(
    AutoDBConfig, load_config("zootopia/config/autodb.yaml", config_type=AutoDBConfig)
)

UserIDType = Enum(
    "UserIDType", [(field, field) for field in _UserIDConfig.model_fields]
)
