from typing import List
from zootopia.core.logger import logger
from zootopia.core.schema import Tables, MessageTableModel
from zootopia.controller.context.context import ContextManager

class ShortTermHistory:
    """
    The short term history is the most recent messages -> in future, series of events.
    An agent can send this in the prompt or use it for other purpose.
    """

    def __init__(self, context):
        """
        Initialize the empty list of events
        """
        self.context: ContextManager = context
        self.messages: List[MessageTableModel] = []

    def get_recent_messages(self, count: int = 10) -> List[MessageTableModel]:
        """
        Get the most recent messages for a given room ID.

        Args:
        - count (int): The number of recent messages to fetch. Defaults to 10.

        Returns:
        - List[MessageTableModel]: A list of the most recent messages for the room.
        """
        try:
            messages = self.context.database.get_multiple_rows(
                table_name=Tables.MESSAGES.value,
                max_rows=count,
                order_by=Tables.MESSAGES__created_at.value,
                order_desc=True,
                conditions=[(Tables.MESSAGES__room_id.value, self.context.room.id)]
            )
            
            # Convert database results to MessageTableModel instances
            self.messages = [MessageTableModel(**message) for message in messages]

            # Reverse the list to get chronological order (oldest to newest)
            self.messages.reverse()

            return self.messages
        except Exception as e:
            logger.error(f"Error fetching recent messages for room {self.context.room.id}: {str(e)}")
            return []