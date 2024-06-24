from datetime import datetime, timezone
from typing import Union

from oauth2client.client import OAuth2Credentials

from src.config.config import config
from src.database.models import GAuthTable, UserTable
from src.database.supabasedb import SupabaseDB
from src.gsuite.gauth.gauth import GAuth
from src.messaging.basemessaging import BaseMessaging
from src.messaging.models import Message, MessageMedium
from src.utils.logger import logger
from src.utils.utils import render_jinja_template


class SignupManager:
    def __init__(
        self,
        messaging_service: BaseMessaging,
        message: Message,
        uid: Union[int, str],
        database: SupabaseDB,
    ) -> None:
        self.messaging_service = messaging_service
        self.database = database
        self.message = message
        self.uid = uid
        self.creds = None

    def verify_user_in_database(self) -> bool:
        conversion = None
        if self.message.medium == MessageMedium.TELEGRAM:
            conversion = config.DATABASE_CONFIG.CONSTANT_IDS.USER_IDS.TELEGRAM

        return self.database.set_user(uid=self.uid, needs_conversion_from=conversion)

    def verify_gauth_in_database(self) -> bool:
        data, _ = self.database.get_rows(
            config.DATABASE_CONFIG.CONSTANT_IDS.TABLE_IDS.GAUTH, max_rows=1
        )

        if len(data[1]) == 0:
            return False

        user_creds = data[1][0]
        creds = OAuth2Credentials(
            access_token=user_creds["access_token"],
            client_id=config.CALENDAR_CONFIG.GOOGLE.GOOGLE_CLIENT_ID,
            client_secret=config.CALENDAR_CONFIG.GOOGLE.GOOGLE_CLIENT_SECRET,
            refresh_token=user_creds["refresh_token"],
            token_expiry=datetime.fromisoformat(user_creds["token_expiry"]).replace(
                tzinfo=None
            ),
            token_uri=user_creds["token_uri"],
            user_agent=user_creds["user_agent"],
        )

        if creds.access_token_expired:
            return False

        self.creds = creds
        return True

    def save_user_to_database(self):
        if self.message.medium == MessageMedium.TELEGRAM:
            user_table = UserTable(
                telegram_id=self.message.uid, username=self.message.user_name
            )
            return self.database.append_row(
                self.database.user_table, row_data=user_table.model_dump()
            )
        else:
            raise NotImplementedError(
                f"SignupManager not configured for {self.message.medium} messages yet."
            )

    async def send_welcome_message(self):
        signup_message = render_jinja_template(
            "signup.jinja",
            "src/manager/signup/templates",
            user_name=self.message.user_name,
        )
        self.database.append_row(
            config.DATABASE_CONFIG.CONSTANT_IDS.TABLE_IDS.MESSAGE,
            {"id": self.database.user_id, "from_bot": True, "message": signup_message},
        )
        return await self.messaging_service.send_message(signup_message, self.uid)

    async def auth_google(self):
        gauth = GAuth.from_config(config.CALENDAR_CONFIG.GOOGLE)
        auth_url = gauth.get_auth_url()
        gauth_message = render_jinja_template(
            "gauth.jinja", "src/manager/signup/templates", gauth_url=auth_url
        )
        try:
            potential_auth_code = self.message.message.message.text
            creds = gauth.authenticate_with_code(potential_auth_code)
        except Exception as e:
            logger.info(  # pylint: disable=W1203
                f"An error occured while authenticating with Google: {e}"
            )
            return await self.messaging_service.send_message(gauth_message, self.uid)

        self.creds = creds
        gauth_table = config.DATABASE_CONFIG.CONSTANT_IDS.TABLE_IDS.GAUTH
        gauth_row = GAuthTable(
            access_token=creds.access_token,
            refresh_token=creds.refresh_token,
            token_expiry=creds.token_expiry.astimezone(timezone.utc).isoformat(),
            token_uri=creds.token_uri,
            user_agent=creds.user_agent,
        )
        json_gauth = gauth_row.model_dump()
        json_gauth[config.DATABASE_CONFIG.CONSTANT_IDS.ID_COLUMN_NAME] = (
            self.database.user_id
        )
        self.database.append_row(gauth_table, json_gauth)

    async def send_successful_auth_message(self):
        signup_message = render_jinja_template(
            "success.jinja",
            "src/manager/signup/templates",
            user_name=self.message.user_name,
        )
        self.database.append_row(
            config.DATABASE_CONFIG.CONSTANT_IDS.TABLE_IDS.MESSAGE,
            {"id": self.database.user_id, "from_bot": True, "message": signup_message},
        )
        return await self.messaging_service.send_message(signup_message, self.uid)
