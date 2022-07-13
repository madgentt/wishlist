"""This module provides the Wishlist database functionality."""
# wishlist/database.py

import configparser
from pathlib import Path
from wishlist import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_wishs.json"
)

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the wishes database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create the wishes database."""
    try:
        db_path.write_text("[]")  # Empty wishes list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR