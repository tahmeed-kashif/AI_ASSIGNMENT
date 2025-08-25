from __future__ import annotations

import sys
import click
from dotenv import load_dotenv

from .config import load_settings
from .db import get_connection, init_db, add_subscriber, list_all_subscribers, set_active


@click.group()
def cli():
    pass


@cli.command()
def init_db_cmd():
    """Initialize the SQLite database."""
    load_dotenv()
    settings = load_settings()
    conn = get_connection(settings.db_path)
    init_db(conn)
    click.echo(f"DB initialized at {settings.db_path}")


@cli.command()
@click.option("--phone", required=True, help="International number, digits only e.g. 15551234567")
@click.option("--name", required=False, help="Optional display name")
def add(phone: str, name: str | None):
    """Add or reactivate a subscriber."""
    load_dotenv()
    settings = load_settings()
    conn = get_connection(settings.db_path)
    add_subscriber(conn, phone, name)
    click.echo(f"Added/activated {phone}")


@cli.command()
@click.option("--phone", required=True)
def deactivate(phone: str):
    load_dotenv()
    settings = load_settings()
    conn = get_connection(settings.db_path)
    set_active(conn, phone, False)
    click.echo(f"Deactivated {phone}")


@cli.command()
@click.option("--phone", required=True)
def activate(phone: str):
    load_dotenv()
    settings = load_settings()
    conn = get_connection(settings.db_path)
    set_active(conn, phone, True)
    click.echo(f"Activated {phone}")


@cli.command()
def list():  # noqa: A003 - click command name
    load_dotenv()
    settings = load_settings()
    conn = get_connection(settings.db_path)
    rows = list_all_subscribers(conn)
    for r in rows:
        status = "active" if r["active"] else "inactive"
        click.echo(f"{r['phone']}\t{r['name'] or ''}\t{status}")


if __name__ == "__main__":
    # Allows: python -m app.cli ...
    sys.argv[0] = "app.cli"
    cli()

