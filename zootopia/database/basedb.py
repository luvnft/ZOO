from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict


class BaseDB(ABC):
    """
    Base class for database operations.
    """

    @abstractmethod
    def insert(
        self,
        table_name: str,
        row_data: Dict[str, Any],
    ):
        pass

    @abstractmethod
    def update(self, table_name: str, item_id: str, item: Dict[str, Any]):
        pass

    @abstractmethod
    def get_rows(self, table_name: str, max_rows: int = 10, from_time: datetime = None):
        pass
