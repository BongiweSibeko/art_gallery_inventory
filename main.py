"""Command-line program for the Art Gallery Inventory Tracker."""

from pathlib import Path

from gallery.artwork import Artwork
from gallery.storage import load_inventory, save_inventory


DATA_FILE = Path(__file__).parent / "data" / "artworks.csv"


def print_menu():
    print("\nART GALLERY INVENTORY TRACKER")
    print("1. View all artworks")
    print("2. Add artwork")
    print("3. Search by artist")
    print("4. Sell artwork")
    print("5. View inventory summary")
    print("6. Exit")


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
            save_inventory(inventory, DATA_FILE)
            print("Inventory saved. Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
