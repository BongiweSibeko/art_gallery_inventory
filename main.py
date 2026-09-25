"""Command-line program for the Art Gallery Inventory Tracker."""

import os
from pathlib import Path

from gallery.artwork import Artwork
from gallery.cloud_storage import CloudStorageError, S3CloudStorage
from gallery.storage import load_inventory, save_inventory


DATA_FILE = Path(__file__).parent / "data" / "artworks.db"
DEFAULT_CLOUD_KEY = "backups/artworks.db"


def print_menu():
    print("\nART GALLERY INVENTORY TRACKER")
    print("1. View all artworks")
    print("2. Add artwork")
    print("3. Search by artist")
    print("4. Sell artwork")
    print("5. View inventory summary")
    print("6. Back up inventory to cloud")
    print("7. Restore inventory from cloud")
    print("8. Exit")


def view_all(inventory):
    if not inventory.artworks:
        print("No artworks found.")
        return

    for artwork in inventory.artworks:
        print(artwork)


def add_artwork(inventory):
    artwork_id = input("Artwork ID: ")
    title = input("Title: ")
    artist = input("Artist: ")
    price = input("Price in rand: ")

    try:
        artwork = Artwork(artwork_id, title, artist, price)
        inventory.add_artwork(artwork)
        print("Artwork added successfully.")
    except ValueError as error:
        print(f"Could not add artwork: {error}")


def search_artworks(inventory):
    artist_name = input("Artist name: ")
    results = inventory.search_by_artist(artist_name)

    if not results:
        print("No matching artworks found.")
        return

    for artwork in results:
        print(artwork)


def sell_artwork(inventory):
    artwork_id = input("Artwork ID to sell: ")
    try:
        artwork = inventory.sell_artwork(artwork_id)
        print(f"'{artwork.title}' has been marked as sold.")
    except ValueError as error:
        print(f"Could not sell artwork: {error}")


def show_summary(inventory):
    print(f"Total artworks: {len(inventory.artworks)}")
    print(f"Available: {inventory.count_by_status('available')}")
    print(f"Sold: {inventory.count_by_status('sold')}")
    print(f"Available inventory value: R{inventory.total_available_value():,.2f}")


def _cloud_storage_from_environment():
    """Create cloud storage using settings kept outside the source code."""
    bucket_name = os.getenv("ART_GALLERY_S3_BUCKET", "").strip()
    if not bucket_name:
        raise CloudStorageError(
            "ART_GALLERY_S3_BUCKET is not set. Set it to your S3 bucket name first."
        )
    return S3CloudStorage(bucket_name)


def backup_to_cloud(inventory):
    """Save the latest data locally, then upload the SQLite file to S3."""
    try:
        save_inventory(inventory, DATA_FILE)
        cloud = _cloud_storage_from_environment()
        key = os.getenv("ART_GALLERY_S3_KEY", DEFAULT_CLOUD_KEY)
        cloud.backup_file(DATA_FILE, key)
        print(f"Cloud backup completed: s3://{cloud.bucket_name}/{key.lstrip('/')}")
    except (CloudStorageError, FileNotFoundError, ValueError) as error:
        print(f"Could not create cloud backup: {error}")


def restore_from_cloud():
    """Download the SQLite database from S3 and load it into memory."""
    try:
        cloud = _cloud_storage_from_environment()
        key = os.getenv("ART_GALLERY_S3_KEY", DEFAULT_CLOUD_KEY)
        cloud.restore_file(DATA_FILE, key)
        inventory = load_inventory(DATA_FILE)
        print("Cloud backup restored successfully.")
        return inventory
    except (CloudStorageError, ValueError) as error:
        print(f"Could not restore cloud backup: {error}")
        return None


def main():
    inventory = load_inventory(DATA_FILE)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all(inventory)
        elif choice == "2":
            add_artwork(inventory)
        elif choice == "3":
            search_artworks(inventory)
        elif choice == "4":
            sell_artwork(inventory)
        elif choice == "5":
            show_summary(inventory)
        elif choice == "6":
            backup_to_cloud(inventory)
        elif choice == "7":
            restored_inventory = restore_from_cloud()
            if restored_inventory is not None:
                inventory = restored_inventory
        elif choice == "8":
            save_inventory(inventory, DATA_FILE)
            print("Inventory saved. Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()
