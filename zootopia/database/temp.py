 def configure_room(
        self, received_message: ReceivedTelegramMessage | ReceivedBirdMessage
    ) -> int:
        """Given messaging request data, set the room id."""

        # TODO: Telegram: given chat_id telegram_user_id (user), get room id
        # Current request_body schema:
        # {
        #     "update_id": int,
        #     "message": {
        #         "message_id": int,
        #         "from": {
        #             "id": int,
        #             "is_bot": bool,
        #             "first_name": str,
        #             "last_name": str,
        #             "language_code": str,
        #         },
        #         "chat": {
        #             "id": int,
        #             "first_name": str,
        #             "last_name": str,
        #             "type": str,
        #         },
        #         "date": int,
        #         "text": str,
        #     },
        # }
        if isinstance(received_message, ReceivedTelegramMessage):
            user_id = received_message.user_id
            room_data, _ = (
                self.table("rooms")
                .select("id")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            if room_data:
                return room_data["id"]
        elif isinstance(received_message, ReceivedBirdMessage):
            user_phone = received_message.user_phone
            channel_id = received_message.channel_id
            user_id = self.users_table.get_id_from_phone(user_phone)
            room_id = self.rooms_table.get_room_id_from_received_bird_message(
                user_id, channel_id
            )
            self.set_room(room_id)