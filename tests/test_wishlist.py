import json
import pytest
from typer.testing import CliRunner

from wishlist import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    wishlist,
)

test_data1 = {
    "description": ["Thing", "1"],
    "link": "link1",
    "price": 1,
    "wish": {
        "Description": "Thing 1",
        "Link": "link1",
        "Price": 1,
    },
}
test_data2 = {
    "description": ["Thing", "2"],
    "link": "link2",
    "price": 2,
    "wish": {
        "Description": "Thing 2",
        "Link": "link2",
        "Price": 2,
    },
}


runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    wish = [{"Description": "New laptop", "Link": "http://", "Price": 100}]
    db_file = tmp_path / "wishlist.json"
    with db_file.open("w") as db:
        json.dump(wish, db, indent=4)
    return db_file


@pytest.mark.parametrize(
    "description, link, price, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1["link"],
            test_data1["price"],
            (test_data1["wish"]),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["link"],
            test_data2["price"],
            (test_data2["wish"]),
        ),
    ],
)
def test_add(mock_json_file, description, link, price, expected):
    wishlister = wishlist.Wishlister(mock_json_file)
    assert wishlister.add(description, link, price).wish == expected
    read = wishlister._db_handler.read_wishes()
    assert len(read.wish_list) == 2