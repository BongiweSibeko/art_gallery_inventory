"""SQLite database functions for the inventory tracker."""

import sqlite3
from pathlib import Path

from gallery.artwork import Artwork
from gallery.inventory import GalleryInventory


TABLE_NAME = "artworks"
FIELDNAMES = ["artwork_id", "title", "artist", "price", "status"]


def _connect(file_path):
    """Open a connection and make sure the artworks table exists.

    Note: artwork_id is stored as a plain column, not a PRIMARY KEY. That
    might look like a missing constraint, but it is deliberate: uniqueness
    is a business rule owned by GalleryInventory (see add_artwork), not a
    storage-level concern. If the file ever contains duplicate IDs -
    because it was hand-edited, or written by something else - load_inventory
    should raise a clear ValueError instead of the database silently
    rejecting a row.
    """
    connection = sqlite3.connect(file_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            artwork_id TEXT NOT NULL,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    return connection

def save_inventory(inventory, file_path):
    """Save all artworks to a SQLite database file.

    Any artworks already stored at this path are replaced - this mirrors
    the old CSV behaviour, where saving always rewrote the whole file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = _connect(path)
    try:
        connection.execute(f"DELETE FROM {TABLE_NAME}")
        connection.executemany(
            f"""
            INSERT INTO {TABLE_NAME} (artwork_id, title, artist, price, status)
            VALUES (:artwork_id, :title, :artist, :price, :status)
            """,
            [artwork.to_dict() for artwork in inventory.artworks],
        )
        connection.commit()
    finally:
        connection.close()


def load_inventory(file_path):
    """Load artworks from a CSV file into a GalleryInventory object."""
    inventory = GalleryInventory()
    path = Path(file_path)

    if not path.exists():
        return inventory

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            artwork = Artwork(
                row["artwork_id"],
                row["title"],
                row["artist"],
                float(row["price"]),
                row["status"],
            )
            inventory.add_artwork(artwork)

    return inventory
