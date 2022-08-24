from typing import Any, Dict, NamedTuple
from pathlib import Path

from database import DatabaseHandler


todo = {
    "Description": "New laptop",
    "Link": "http://",
    "Price": 100,
}

class CurrentWish(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Wishlister:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)