import os
from enum import Enum
from typing import cast

import yaml
from pydantic import BaseModel, ValidationError

from src.autodb.models import AutoDBConfig
from src.database.models import ConstantIDConfig, SupabaseConfig, _UserIDConfig
from src.gsuite.models import GAuthConfig
from src.messaging.models import TelegramBotConfig


class CalendarConfig(BaseModel):
    GOOGLE: GAuthConfig
    CALENDAR_NAME: str
    CALENDAR_DESCRIPTION: str


class MessagingConfig(BaseModel):
    TELEGRAM: TelegramBotConfig


class DatabaseConfig(BaseModel):
    SUPABASE: SupabaseConfig
    CONSTANT_IDS: ConstantIDConfig


class UploadConfig(BaseModel):
    FOLDER_NAME: str
    FILE_NAME_FORMAT: str


class AIAssistantConfig(BaseModel):
    CALENDAR_CONFIG: CalendarConfig
    MESSAGING_CONFIG: MessagingConfig
    DATABASE_CONFIG: DatabaseConfig
    UPLOAD_CONFIG: UploadConfig
    GOOGLE_API_KEY: str


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
    config_path: str, set_env: bool = False, config_type: BaseModel = AIAssistantConfig
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


testing = False
prefix = "src/config/" if testing else "/etc/secrets/"
config = cast(AIAssistantConfig, load_config(f"{prefix}local.yaml", set_env=True))
autodb_config = cast(
    AutoDBConfig, load_config("src/config/autodb.yaml", config_type=AutoDBConfig)
)

UserIDType = Enum(
    "UserIDType", [(field, field) for field in _UserIDConfig.model_fields]
)
UserTableName = config.DATABASE_CONFIG.CONSTANT_IDS.TABLE_IDS.USER
