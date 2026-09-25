"""Cloud backup helpers for the art gallery inventory.

The project keeps SQLite as its local database. This module adds an optional
cloud-computing feature: backing the database up to, and restoring it from,
Amazon S3-compatible object storage.
"""

from pathlib import Path


class CloudStorageError(RuntimeError):
    """Raised when a cloud backup or restore cannot be completed."""


class S3CloudStorage:
    """Small wrapper around an S3 client.

    A client can be injected for unit tests. In normal use, boto3 creates the
    client and uses the standard AWS credential chain (environment variables,
    ~/.aws/credentials, IAM role, and so on).
    """

    def __init__(self, bucket_name, client=None):
        bucket_name = str(bucket_name).strip()
        if not bucket_name:
            raise ValueError("Cloud bucket name cannot be empty")

        self.bucket_name = bucket_name
        self.client = client if client is not None else self._create_client()

    @staticmethod
    def _create_client():
        try:
            import boto3
        except ImportError as error:
            raise CloudStorageError(
                "Cloud support needs boto3. Install dependencies with "
                "'python3 -m pip install -r requirements.txt'."
            ) from error

        return boto3.client("s3")

    def backup_file(self, local_file, object_key="backups/artworks.db"):
        """Upload a local file to the configured S3 bucket."""
        path = Path(local_file)
        if not path.exists():
            raise FileNotFoundError(f"Local file was not found: {path}")
        if not path.is_file():
            raise ValueError(f"Local path is not a file: {path}")

        key = self._clean_key(object_key)
        try:
            self.client.upload_file(str(path), self.bucket_name, key)
        except Exception as error:
            raise CloudStorageError(f"Cloud backup failed: {error}") from error

        return key

    def restore_file(self, local_file, object_key="backups/artworks.db"):
        """Download a database backup from S3 to a local file."""
        path = Path(local_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        key = self._clean_key(object_key)

        try:
            self.client.download_file(self.bucket_name, key, str(path))
        except Exception as error:
            raise CloudStorageError(f"Cloud restore failed: {error}") from error

        return path

    @staticmethod
    def _clean_key(object_key):
        key = str(object_key).strip().lstrip("/")
        if not key:
            raise ValueError("Cloud object key cannot be empty")
        return key
