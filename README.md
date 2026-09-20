# Art Gallery Inventory Tracker

A beginner-friendly Python project for managing artwork in a small gallery.

This version is intentionally much simpler than a full data-engineering platform. It focuses on entry-level skills that are easier to explain in an interview or assessment:

- Python classes and objects
- Lists and loops
- Functions and simple validation
- Reading and writing CSV files
- Error handling with `try` / `except`
- Unit testing with Python's built-in `unittest`

## Features

The program can:

1. View all artworks
2. Add a new artwork
3. Search for artworks by artist
4. Mark an artwork as sold
5. Show the number of available and sold artworks
6. Calculate the total value of available artworks
7. Save and load inventory from a CSV file

## Project structure

```text
art_gallery_inventory_entry_level/
├── gallery/
│   ├── __init__.py
│   ├── artwork.py       # Artwork class
│   ├── inventory.py     # Inventory business logic
│   └── storage.py       # CSV save/load functions
├── data/
│   └── artworks.csv     # Sample data
├── tests/
│   ├── test_artwork.py
│   ├── test_inventory.py
│   └── test_storage.py
├── main.py              # Console application
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer is recommended.
- No external packages are required.

## Run the program

From the project folder:

```bash
python main.py
```

On some Linux systems, use:

```bash
python3 main.py
```

## Run the unit tests

```bash
python -m unittest discover -s tests -v
```

or:

```bash
python3 -m unittest discover -s tests -v
```

You can also open a test file in IntelliJ IDEA or PyCharm and use the green run button next to a test class or test method once the Python SDK is configured.

## Example concepts covered by the tests

- New artworks start as available.
- Negative prices are rejected.
- Duplicate artwork IDs are rejected.
- An artwork can be found by its ID.
- Artist searches are case-insensitive.
- Selling an artwork changes its status.
- An artwork cannot be sold twice.
- Available inventory value is calculated correctly.
- Inventory can be saved to and loaded from CSV.

## Possible beginner extensions

Once the basic project is comfortable, you can add:

- Search by title
- Update an artwork's price
- Sort artworks by price
- Add a simple login
- Replace CSV storage with SQLite
- Build a small Flask web interface

## Unit Tests

The project includes ** unit tests** using Python's built-in `unittest` module.

- `tests/test_artwork.py` - artwork validation, status, formatting, and dictionary conversion
- `tests/test_inventory.py` - adding, finding, searching, selling, removing, counting, and inventory value
- `tests/test_storage.py` - CSV saving/loading, file creation, data preservation, and invalid data

Run the complete test suite with:

```bash
python -m unittest discover -s tests -v
```

Expected result: `Ran tests` followed by `OK`.
