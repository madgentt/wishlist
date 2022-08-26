"""This module provides the Wishlist CLI."""
# wishlist/cli.py

from pathlib import Path
import typer
import os
from typing import List, Optional
from wishlist import (ERRORS, __app_name__,
                      __version__, config, database, wishlist)

app = typer.Typer()


@app.command()
def add(
    description: List[str] = typer.Argument(...),
    link: str = typer.Option("--link", "-l"),
    price: int = typer.Option(2, "--price", "-p", min=1, max=3)
) -> None:
    """Add a new wish with a DESCRIPTION."""
    wishlister = get_wishlister()
    wish, error = wishlister.add(description, link, price)
    if error:
        typer.secho(
            f'Adding wish failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""wish: "{wish['Description']}" was added """
            f"""with priority: {price}""",
            fg=typer.colors.GREEN,
        )


def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH) + "/." + Path.home().stem + "_wishes.json",
        "--db-path",
        "-db",
        prompt="Wishes database location?",
    ),
) -> None:
    """Initialize the wishes database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The wishes database is {db_path}", fg=typer.colors.GREEN)


def get_wishlister() -> wishlist.Wishlister:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "wishlist init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return wishlist.Wishlister(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "wishlist init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return