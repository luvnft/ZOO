import os
import tempfile
from datetime import datetime, timedelta
from typing import Union

from oauth2client.client import OAuth2Credentials
from tzlocal import get_localzone

from src.config.config import config
from src.database.supabasedb import SupabaseDB
from src.gsuite.gcal.gcal import GCal
from src.gsuite.gdrive.gdrive import GDrive
from src.messaging.basemessaging import BaseMessaging
from src.messaging.models import Message
from src.messaging.telegrambot import TelegramBot
from src.utils.utils import render_jinja_template


class UploadManager:
    def __init__(
        self,
        messaging_service: BaseMessaging,
        message: Message,
        database: SupabaseDB,
    ) -> None:
        self.messaging_service = messaging_service
        self.database = database
        self.message = message
        self.uid = uid
        self.creds = None
        self.upload_url = None

    async def upload_to_drive(self):
        file = await TelegramBot.download_file_from_message(
            self.messaging_service, self.message.message.message
        )

        if file is None:
            raise ValueError("File not downloaded from Telegram message properly")

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        gdrive = GDrive(self.creds)
        folder_id = gdrive.get_or_create_folder(config.UPLOAD_CONFIG.FOLDER_NAME)
        file_name = datetime.now().strftime(config.UPLOAD_CONFIG.FILE_NAME_FORMAT)
        self.upload_url = gdrive.upload_file(file_name, temp_file_path, folder_id)

        os.remove(temp_file_path)

    def save_upload_url_to_calendar(self):
        gcal = GCal(self.creds)
        calendar_id = gcal.get_or_create_calendar(
            config.CALENDAR_CONFIG.CALENDAR_NAME,
            config.CALENDAR_CONFIG.CALENDAR_DESCRIPTION,
        )

        start_time = datetime.now(get_localzone())
        end_time = start_time + timedelta(minutes=20)

        gcal.add_event(
            title="🗂️ Saved Document",
            description=f"Link to the saved document on drive:\n{self.upload_url}",
            start_time=start_time,
            end_time=end_time,
            calendar_id=calendar_id,
        )

    async def send_uploaded_notification(self):
        upload_message = render_jinja_template(
            "success.jinja",
            "src/manager/upload/templates",
            folder_name=config.UPLOAD_CONFIG.FOLDER_NAME,
            upload_url=self.upload_url,
        )
        self.database.insert(
            config.DATABASE_CONFIG.CONSTANT_IDS.TABLE_IDS.MESSAGE,
            {"id": self.database.user_id, "from_bot": True, "message": upload_message},
        )
        return await self.messaging_service.send_message(upload_message)
