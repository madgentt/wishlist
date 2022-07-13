"""Wishlist entry point script."""
# wishlist/__main__.py

from wishlist import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
