"""Class used to store utils needed for agent_controller logic"""

from config.config import ZootopiaConfig
from zootopia.core.schema import Tables, AgentTableModel, RoomTableModel, UserTableModel
from zootopia.storage.database.supabase import SupabaseDB
from zootopia.platform.platform import MessageProviderBase
from zootopia.platform.sms.bird import BirdSMSProvider
from zootopia.platform.models import (
    BirdMetadata,
    MessageProvider,
    TelegramMetadata,
    ZootopiaMessage,
)
from zootopia.platform.telegram.telegram import Telegram

class ContextManager:
    def __init__(self, request_body, config: ZootopiaConfig):
        """
        1. Init database
        2. Init correct messaging service given the message
        3. Use messaging service to format it into a ZootopiaMessage object
        4. Use ZootopiaMessage to locate correct user, room & store in ZootopiaAppState variables
        """
        self.database: SupabaseDB = SupabaseDB.from_config(
            config.DATABASE_CONFIG.SUPABASE
        )
        self.messaging_service: MessageProviderBase = self._create_messaging_provider(
            request_body, config
        )
        self.message: ZootopiaMessage = self.messaging_service.receive_message(
            request_body
        )
        self.user: UserTableModel = self._get_or_create_user_from_db(self.message)
        self.agent: AgentTableModel = self._get_or_create_agent_from_db(self.message)
        self.room: RoomTableModel = self._get_or_create_room_from_db(
            self.message, self.user, self.agent
        )

    def _create_messaging_provider(
        self, request_body, config: ZootopiaConfig
    ) -> MessageProviderBase:
        """Returns correct messaging service based on the request body"""
        if "payload" in request_body:
            return BirdSMSProvider.from_config(config.MESSAGING_CONFIG.BIRD)
        elif "update_id" in request_body:
            return TelegramBot.from_config(config.MESSAGING_CONFIG.TELEGRAM)
        else:
            raise NotImplementedError("Messaging platform not implemented yet.")

    def _get_or_create_user_from_db(self, message: ZootopiaMessage) -> UserTableModel:
        """Returns user object from database using message metadata"""
        user = None

        # Get user
        if message.provider == MessageProvider.TELEGRAM:
            user = self.database.get_row(
                Tables.USERS.value,

                (Tables.USERS__telegram_uid.value, message.metadata.uid),
            )
        elif message.provider == MessageProvider.BIRD:
            user = self.database.get_row(
                Tables.USERS.value,

                (Tables.USERS__phone_number.value, message.metadata.phone_number),
            )

        # If no user exists, create user
        if not user:
            new_user = UserTableModel(
                telegram_uid=(
                    message.metadata.uid
                    if isinstance(message.metadata, TelegramMetadata)
                    else None
                ),
                phone_number=(
                    message.metadata.phone_number
                    if isinstance(message.metadata, BirdMetadata)
                    else None
                ),
            )

            user = self.database.insert(Tables.USERS.value, new_user)

        return user

    def _get_or_create_agent_from_db(self, message: ZootopiaMessage) -> AgentTableModel:
        """Returns agent object from database using message metadata"""
        agent: AgentTableModel = None

        # Get agent
        if message.provider == MessageProvider.TELEGRAM:
            agent = self.database.get_row(
                Tables.AGENTS.value,
            )
        elif message.provider == MessageProvider.BIRD:
            agent = self.database.get_row(
                Tables.AGENTS.value,
                (Tables.AGENTS__bird_channel_id.value, message.metadata.channel_id),
            )

        # If no agents exists, create one
        if not agent:
            new_agent = AgentTableModel(
                telegram_chat_id=(
                    message.metadata.chat_id
                    if isinstance(message.metadata, TelegramMetadata)
                    else None
                ),
                bird_channel_id=(
                    message.metadata.channel_id
                    if isinstance(message.metadata, BirdMetadata)
                    else None
                ),
            )

            agent = self.database.insert(Tables.AGENTS.value, new_agent)

        return agent

    def _get_or_create_room_from_db(
        self, message: ZootopiaMessage, user: UserTableModel, agent: AgentTableModel
    ) -> RoomTableModel:
        """Returns room object from database using message metadata"""
        room = None

        # Get the room via message metadata
        room = self.database.get_row(
            Tables.ROOMS.value,
            (Tables.ROOMS__user_id.value, user.id),

            (Tables.ROOMS__agent_id.value, agent.id),
        )

        # If no room exists, create room via message metadata
        if not room:
            new_room = RoomTableModel(user_id=user.id, agent_id=agent.id)
            user = self.database.insert(Tables.ROOMS.value, new_room)
        return room
