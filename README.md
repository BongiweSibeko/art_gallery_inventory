# Art Gallery Inventory Tracker

A beginner-friendly Python project for managing artwork in a small gallery.

This version is intentionally much simpler than a full data-engineering platform. It focuses on entry-level skills that are easier to explain in an interview or assessment:

- Python classes and objects
- Lists and loops
- Functions and simple validation
- Reading and writing a SQLite database with Python's built-in `sqlite3` module
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
7. Save and load inventory from a SQLite database

## Project structure

```text
art_gallery_inventory_entry_level/
├── gallery/
│   ├── __init__.py
│   ├── artwork.py       # Artwork class
│   ├── inventory.py     # Inventory business logic
│   └── storage.py       # SQLite save/load functions
├── data/
│   └── artworks.db      # Sample data
├── tests/
│   ├── test_artwork.py
│   ├── test_inventory.py
│   └── test_storage.py
├── main.py              # Console application
├── requirements.txt
└── README.md
```

## A note on `storage.py`

The `artwork_id` column in the database is **not** set up as a primary key,
even though IDs are supposed to be unique. That's deliberate: uniqueness is a
rule about the *business* (an inventory shouldn't have two artworks with the
same ID), not about the *file format*. That rule lives in
`GalleryInventory.add_artwork`, and `load_inventory` calls that same method
when reading rows back in — so if a `.db` file is ever hand-edited to contain
a duplicate ID, loading it raises a clear `ValueError` instead of failing
somewhere else, or silently letting it through.

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
- Inventory can be saved to and loaded from a SQLite database.

## Possible beginner extensions

Once the basic project is comfortable, you can add:

- Search by title
- Update an artwork's price
- Sort artworks by price
- Add a simple login
- Add a second table (e.g. exhibitions) and query across both
- Build a small Flask web interface

## Unit Tests

The project includes **89 unit tests** using Python's built-in `unittest` module.

- `tests/test_artwork.py` - artwork validation, status, formatting, and dictionary conversion
- `tests/test_inventory.py` - adding, finding, searching, selling, removing, counting, and inventory value
- `tests/test_storage.py` - SQLite saving/loading, file creation, data preservation, and invalid data

Run the complete test suite with:

```bash
python -m unittest discover -s tests -v
```

Expected result: `Ran 89 tests` followed by `OK`.
