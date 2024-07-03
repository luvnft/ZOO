from typing import Any, Dict, Optional, Union, List, Type, TypeVar, Generic, Literal
from pydantic import BaseModel
from supabase import create_client
from src.messaging.models import Message
from src.config.config import UserIDType
from src.database.basedb import BaseDB
from src.database.models import SupabaseConfig, TableModel, TABLE_MODEL_MAP
from datetime import datetime

T = TypeVar('T', bound=TableModel)

class SupabaseDB(BaseDB):
    def __init__(self, url: str, key: str) -> None:
        self.supabase = create_client(url, key)
        self.user_id = None
        self.agent_id = None
        self.room_id = None

    def set_variables(self, room_id: int, user_id: int, agent_id: int) -> None:
        self.room_id = room_id
        self.user_id = user_id
        self.agent_id = agent_id

    @classmethod
    def from_config(cls, config: SupabaseConfig):
        return cls(url=config.URL, key=config.KEY)

    def insert(self, table_name: str, item: TableModel) -> TableModel:
        data, _ = self.supabase.table(table_name).insert(item.model_dump()).execute()
        return type(item)(**data[1][0]) if data and data[1] else None

    def update(self, table_name: str, item_id: int, item: TableModel) -> TableModel:
        data, _ = self.supabase.table(table_name).update(item.model_dump()).eq("id", item_id).execute()
        return type(item)(**data[1][0]) if data and data[1] else None

    def get_row(self, table_name: str, **filters) -> Optional[TableModel]:
        """
        Fetch a single row from the specified table based on the given filters.
        """
        model = TABLE_MODEL_MAP[table_name]
        query = self.supabase.table(table_name).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        
        data, _ = query.limit(1).single().execute()
        return model(**data[1]) if data and data[1] else None

    def get_multiple_rows(self, 
                 table_name: str, 
                 max_rows: int = 10, 
                 from_time: Optional[datetime] = None, 
                 order_by: str = "created_at",
                 order_desc: bool = True,
                 **filters) -> List[TableModel]:
        """
        Fetch multiple rows from the specified table based on the given filters and parameters.
        """
        model = TABLE_MODEL_MAP[table_name]
        query = self.supabase.table(table_name).select("*")

        # Apply filters
        for key, value in filters.items():
            query = query.eq(key, value)

        # Apply time filter if specified
        if from_time is not None:
            query = query.gte("created_at", from_time.isoformat())

        # Apply ordering
        query = query.order(order_by, desc=order_desc)

        # Apply limit
        query = query.limit(max_rows)

        data, _ = query.execute()

        return [model(**item) for item in data[1]] if data and data[1] else []

    def delete(self, table_name: str, item_id: int) -> bool:
        data, _ = self.supabase.table(table_name).delete().eq("id", item_id).execute()
        return bool(data and data[1])

    def query(self, table_name: str, **filters) -> List[TableModel]:
        model = TABLE_MODEL_MAP[table_name]
        query = self.supabase.table(table_name).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        data, _ = query.execute()
        return [model(**item) for item in data[1]] if data and data[1] else []