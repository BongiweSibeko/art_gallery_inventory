# Art Gallery Inventory Tracker

A Python project for managing artwork in a small gallery. It also includes an optional cloud-computing feature for backing up and restoring the SQLite inventory database with Amazon S3.

## What it covers

- Python classes and objects
- Lists, loops, functions, and validation
- SQLite with Python's built-in `sqlite3` module
- Error handling with `try` / `except`
- Unit testing with `unittest`
- Cloud object storage with Amazon S3
- Environment variables for cloud configuration
- Separation between local storage and cloud storage

## Features

The program can:

1. View all artworks
2. Add a new artwork
3. Search for artworks by artist
4. Mark an artwork as sold
5. Show inventory totals and available value
6. Save and load inventory from a local SQLite database
7. Back up the SQLite database to Amazon S3
8. Restore the SQLite database from Amazon S3

## Project structure

```text
art_gallery_inventory/
├── gallery/
│   ├── __init__.py
│   ├── artwork.py
│   ├── inventory.py
│   ├── storage.py          # Local SQLite storage
│   └── cloud_storage.py    # AWS S3 backup/restore
├── data/
│   └── artworks.db
├── tests/
│   ├── test_artwork.py
│   ├── test_inventory.py
│   ├── test_storage.py
│   └── test_cloud_storage.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- `boto3` for AWS S3 cloud support

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run locally

```bash
python3 main.py
```

The local inventory features work with the SQLite database in `data/artworks.db` — no cloud setup needed for that part.

## Cloud backup setup

The cloud backup feature assumes an S3 bucket already exists and that AWS credentials are available through the normal channels — `aws configure`, environment variables, or an IAM role. `boto3` picks these up automatically, so the app never stores AWS keys itself.

Point the app at the bucket:

```bash
export ART_GALLERY_S3_BUCKET="my-art-gallery-backups"
```

Optionally override where the backup lives inside the bucket:

```bash
export ART_GALLERY_S3_KEY="backups/artworks.db"
```

(`backups/artworks.db` is already the default, so this only matters if you want to change it.)

Then run the app and choose:

- **6** to back up the current SQLite inventory to S3
- **7** to restore the inventory from S3

## How the cloud feature works

The application always uses SQLite locally. When a cloud backup is requested:

```text
GalleryInventory
      |
      v
SQLite database (local)
      |
      v
cloud_storage.py
      |
      v
Amazon S3 bucket (cloud)
```

It's a simple hybrid storage setup: the app works fully on its own locally, and the S3 backup is there for durability and recovery if the local file is ever lost.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

The S3 tests use a fake S3 client, so running the suite doesn't upload anything to AWS and doesn't need real cloud credentials.

## Security notes

- No AWS access keys are hard-coded in the Python files.
- `.env` files, credential files, and secret keys are not committed to Git.
- The AWS user/role only needs the S3 permissions it actually uses.
- Use a private S3 bucket unless there's a specific reason to make the data public.

WTC Proof for Cloud Computing: WTC-ABC6PJFK
WTC Proof for Data Engineering: WTC-CVPCHCWR

## How I'd explain this feature

The application stores its active inventory in a local SQLite database. I added a cloud layer using Amazon S3 so the database can be backed up remotely and restored after local data loss. I kept credentials outside the source code using AWS's standard credential system and environment variables, and I used dependency injection in the cloud-storage class so I could unit-test it without making real network requests.
