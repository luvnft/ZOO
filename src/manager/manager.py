from typing import Union

from src.config.config import config
from src.database.supabasedb import SupabaseDB
from src.manager.communicate.communicate import CommunicateManager
from src.manager.models import Intents
from src.manager.save.save import SaveManager
from src.manager.signup.signup import SignupManager
from src.manager.upload.upload import UploadManager
from src.manager.cancel.cancel import CancelManager
from src.messaging.basemessaging import BaseMessaging
from src.messaging.models import Message, MessageType
from src.utils.logger import logger


class Manager:
    def __init__(
        self, messaging_service: BaseMessaging, message: Message, uid: Union[int, str]
    ) -> None:
        self.messaging_service = messaging_service
        self.message = message
        self.uid = uid
        self.database = SupabaseDB.from_config(config.DATABASE_CONFIG.SUPABASE)

        self.sm = SignupManager(
            messaging_service=self.messaging_service,
            message=self.message,
            uid=self.uid,
            database=self.database,
        )

        self.up = UploadManager(
            messaging_service=self.messaging_service,
            message=self.message,
            uid=self.uid,
            database=self.database,
        )

        self.cm = CommunicateManager(
            messaging_service=self.messaging_service,
            message=self.message,
            uid=self.uid,
            database=self.database,
        )

        self.sv = SaveManager(
            messaging_service=self.messaging_service,
            message=self.message,
            uid=self.uid,
            database=self.database,
        )

    async def find_intent(self) -> Intents:
        if self.sm.verify_user_in_database() is False:
            logger.info("User is not signed up yet.")
            self.sm.save_user_to_database()
            await self.sm.send_welcome_message()
            return Intents.USER_SIGNUP

        if self.sm.verify_gauth_in_database() is False:
            logger.info("User has unauthenticated Google account.")
            await self.sm.auth_google()
            if self.sm.creds is not None:
                await self.sm.send_successful_auth_message()
            return Intents.AUTH_GOOGLE

        if self.message.type is MessageType.FILE:
            logger.info("User sent a file for upload.")
            self.up.creds = self.sm.creds
            await self.up.upload_to_drive()
            self.up.save_upload_url_to_calendar()
            await self.up.send_uploaded_notification()
            return Intents.SAVE_FILE

        # add relavent data to database
        self.sv.save_data_using_autodb()
        self.sv.save_user_message_to_db()

        if self.sv.user_wants_to_save_data():
            logger.info("User wants to save data.")
            self.sv.creds = self.sm.creds
            self.sv.save_data_to_calendar()
            await self.sv.send_saved_data_notification()

        self.cm.get_relevant_user_data()
        self.cm.get_past_conversation()
        await self.cm.send_llm_response_message()
        return Intents.ANSWER_QUERY

    async def simple_response(self):
        if self.sm.verify_user_in_database() is False:
            logger.info("User is not signed up yet.")
            self.sm.save_user_to_database()
            await self.sm.send_welcome_message()
            return Intents.USER_SIGNUP

        self.cm.get_past_conversation()
        await self.cm.send_llm_response_message()
        return Intents.ANSWER_QUERY
