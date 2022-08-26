from typing import Any, Dict, List, NamedTuple
from pathlib import Path

from wishlist import DB_READ_ERROR
from wishlist.database import DatabaseHandler


class CurrentWish(NamedTuple):
    wish: Dict[str, Any]
    error: int

class Wishlister:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], link, price: int = 2) -> CurrentWish:
        """Add a new wish to the database."""
        description_text = " ".join(description)
        wish = {
            "Description": description_text,
            "Link": link,
            "Price": price,
        }
        read = self._db_handler.read_wishes()
        if read.error == DB_READ_ERROR:
            return CurrentWish(wish, read.error)
        read.wish_list.append(wish)
        write = self._db_handler.write_wishes(read.wish_list)
        return CurrentWish(wish, write.error)