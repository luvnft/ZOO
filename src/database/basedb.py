from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict


class BaseDB(ABC):
    """
    Base class for database operations.
    """

    @abstractmethod
    def append_row(
        self,
        table_name: str,
        row_data: Dict[str, Any],
    ):
        pass

    @abstractmethod
    def update_cell(self, table_name: str, column_name: str, new_value: Any):
        pass

    @abstractmethod
    def get_rows(self, table_name: str, max_rows: int = 10, from_time: datetime = None):
        pass
