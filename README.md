# Art Gallery Inventory Tracker

A beginner-friendly Python project for managing artwork in a small gallery. It now includes an optional **cloud-computing feature** for backing up and restoring the SQLite inventory database with **Amazon S3**.

## Skills demonstrated

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
art_gallery_inventory_entry_level/
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

The normal local inventory features work with the SQLite database in `data/artworks.db`.

## Configure cloud backup

The project deliberately does **not** store AWS passwords or secret keys in source code.

### 1. Create an S3 bucket

Create an Amazon S3 bucket in your AWS account, for example:

```text
my-art-gallery-backups
```

### 2. Configure AWS credentials

You can use the AWS CLI:

```bash
aws configure
```

Or use standard AWS environment variables / IAM credentials. `boto3` automatically follows the normal AWS credential chain.

### 3. Set the bucket name

On Linux/macOS:

```bash
export ART_GALLERY_S3_BUCKET="my-art-gallery-backups"
```

Optional: change the object key used inside the bucket:

```bash
export ART_GALLERY_S3_KEY="backups/artworks.db"
```

The default key is already `backups/artworks.db`, so this second variable is optional.

### 4. Run the application

```bash
python3 main.py
```

Choose:

- **6** to back up the current SQLite inventory to S3.
- **7** to restore the inventory from S3.

## How the cloud feature works

The application still uses SQLite locally. When a cloud backup is requested:

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

This is a simple example of **hybrid storage**: the application can work locally while keeping a remote cloud backup for durability and recovery.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

The S3 unit tests use a fake S3 client, so running the test suite does **not** upload anything to AWS and does not require cloud credentials.

## Security notes

- Do not hard-code AWS access keys in Python files.
- Do not commit `.env`, credential files, or secret keys to Git.
- Give the AWS user/role only the S3 permissions it needs.
- Use a private S3 bucket unless there is a specific reason to make data public.

## Interview explanation

You can describe the feature like this:

> "The application stores its active inventory in a local SQLite database. I added a cloud layer using Amazon S3 so the database can be backed up remotely and restored after local data loss. I kept credentials outside the source code using AWS's standard credential system and environment variables, and I used dependency injection in the cloud-storage class so I could unit-test it without making real network requests."
