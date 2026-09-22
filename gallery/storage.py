"""CSV file functions for the inventory tracker."""

import csv
from pathlib import Path

from gallery.artwork import Artwork
from gallery.inventory import GalleryInventory


FIELDNAMES = ["artwork_id", "title", "artist", "price", "status"]


def save_inventory(inventory, file_path):
    """Save all artworks to a CSV file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for artwork in inventory.artworks:
            writer.writerow(artwork.to_dict())


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
