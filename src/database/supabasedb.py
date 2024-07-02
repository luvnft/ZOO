from datetime import datetime
from typing import Any, Dict, Optional, Union

from supabase import create_client

from src.config.config import UserIDType, UserTableName
from src.database.basedb import BaseDB
from src.database.models import SupabaseConfig

# TODO: set db's room id
class SupabaseDB(BaseDB):
    def __init__(self, url: str, key: str) -> None:
        supabase = create_client(url, key)
        self.supabase = supabase
        self.user_table = UserTableName

        # Variables to keep track of current chatroom
        self.user_id = None
        self.room_id = None
        self.agent_id = None

        # Initialize table classes
        self._users_table = None
        self._agents_table = None
        self._rooms_table = None
        self._messages_table = None
        self._preferences_table = None

    @classmethod
    def from_config(cls, config: SupabaseConfig):
        return cls(url=config.URL, key=config.KEY)

    def append_row(
        self,
        table_name: str,
        row_data: Dict[str, Any],
    ):
        data, count = self.supabase.table(table_name).insert(row_data).execute()
        print(data, count)
        return data, count

    def update_cell(
        self,
        table_name: str,
        column_name: str,
        new_value: Any,
    ):
        data, count = (
            self.supabase.table(table_name)
            .update({column_name: new_value})
            .eq("id", self.user_id)
            .execute()
        )
        return data, count

    def set_user(
        self,
        uid: Union[str, int],
        needs_conversion_from: Optional[UserIDType] = None,
    ) -> bool:
        if needs_conversion_from is not None:
            data, count = (
                self.supabase.table(self.user_table)
                .select("id")
                .eq(needs_conversion_from, uid)
                .execute()
            )

            if data[1] is None or len(data[1]) == 0:
                return False
            if len(data[1]) > 1:
                raise ValueError(
                    f"Multiple users found with {needs_conversion_from.value} ID: {uid}"
                )

            uid = data[1][0]["id"]

        self.user_id = uid
        return True

    def get_rows(self, table_name: str, max_rows: int = 10, from_time: datetime = None):
        query = self.supabase.table(table_name).select("*").eq("id", self.user_id)

        if from_time is not None:
            query = query.gte("created_at", from_time.isoformat())

        query = query.order("created_at", desc=True).limit(max_rows)

        data, count = query.execute()

        return data, count
