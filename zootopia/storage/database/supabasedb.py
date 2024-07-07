
from datetime import datetime
from typing import Any, Dict, Generic, List, Literal, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from supabase import create_client

from config.config import UserIDType
from zootopia.storage.database.basedb import BaseDB
from zootopia.storage.database.models import TABLE_MODEL_MAP, SupabaseConfig, TableModel

T = TypeVar("T", bound=TableModel)


class SupabaseDB(BaseDB):
    def __init__(self, url: str, key: str) -> None:
        self.supabase = create_client(url, key)

    @classmethod
    def from_config(cls, config: SupabaseConfig):
        return cls(url=config.URL, key=config.KEY)

    def insert(self, table_name: str, item: TableModel) -> TableModel:
        # Remove 'id' field, since Supabase auto-increments
        item_dict = item.model_dump(exclude={"id"})
        data, _ = self.supabase.table(table_name).insert(item_dict).execute()
        return type(item)(**data[1][0]) if data and data[1] else None

    def update(self, table_name: str, item: TableModel, *conditions) -> TableModel:
        query = self.supabase.table(table_name).update(item.model_dump())
        for key, value in conditions:
            query = query.eq(key, value)
        data, _ = query.execute()
        return type(item)(**data[1][0]) if data and data[1] else None

    def get_row(self, table_name: str, *conditions) -> Optional[TableModel]:
        query = self.supabase.table(table_name).select("*")
        for key, value in conditions:
            query = query.eq(key, value)

        data, _ = query.limit(1).execute()

        if data and data[1]:
            model_class = TABLE_MODEL_MAP[table_name]
            return model_class(**data[1][0])
        return None

    def get_multiple_rows(
        self,
        table_name: str,
        max_rows: int = 10,
        from_time: Optional[datetime] = None,
        order_by: str = "created_at",
        order_desc: bool = True,
        *conditions
    ) -> List[TableModel]:
        query = self.supabase.table(table_name).select("*")

        for key, value in conditions:
            query = query.eq(key, value)

        if from_time is not None:
            query = query.gte("created_at", from_time.isoformat())

        query = query.order(order_by, desc=order_desc).limit(max_rows)

        data, _ = query.execute()

        model_class = TABLE_MODEL_MAP[table_name]
        return [model_class(**item) for item in data[1]] if data and data[1] else []

    def delete(self, table_name: str, *conditions) -> bool:
        query = self.supabase.table(table_name).delete()
        for key, value in conditions:
            query = query.eq(key, value)
        data, _ = query.execute()
        return bool(data and data[1])

    def query(self, table_name: str, *conditions) -> List[TableModel]:
        query = self.supabase.table(table_name).select("*")
        for key, value in conditions:
            query = query.eq(key, value)
        data, _ = query.execute()
        model_class = TABLE_MODEL_MAP[table_name]
        return [model_class(**item) for item in data[1]] if data and data[1] else []
