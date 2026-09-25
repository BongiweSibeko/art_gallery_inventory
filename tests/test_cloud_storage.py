"""Tests for the optional cloud backup feature."""

import tempfile
import unittest
from pathlib import Path

from gallery.cloud_storage import CloudStorageError, S3CloudStorage


class FakeS3Client:
    def __init__(self):
        self.uploads = []
        self.downloads = []
        self.download_bytes = b"database content"
        self.upload_error = None
        self.download_error = None

    def upload_file(self, filename, bucket, key):
        if self.upload_error:
            raise self.upload_error
        self.uploads.append((filename, bucket, key))

    def download_file(self, bucket, key, filename):
        if self.download_error:
            raise self.download_error
        self.downloads.append((bucket, key, filename))
        Path(filename).write_bytes(self.download_bytes)


class TestS3CloudStorage(unittest.TestCase):
    def test_empty_bucket_name_is_rejected(self):
        with self.assertRaises(ValueError):
            S3CloudStorage("   ", client=FakeS3Client())

    def test_bucket_name_is_trimmed(self):
        cloud = S3CloudStorage("  gallery-backups  ", client=FakeS3Client())
        self.assertEqual("gallery-backups", cloud.bucket_name)

    def test_backup_uploads_to_expected_bucket_and_key(self):
        client = FakeS3Client()
        cloud = S3CloudStorage("gallery-backups", client=client)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            file_path.write_bytes(b"sqlite")
            cloud.backup_file(file_path, "backups/artworks.db")
        self.assertEqual("gallery-backups", client.uploads[0][1])
        self.assertEqual("backups/artworks.db", client.uploads[0][2])

    def test_backup_removes_leading_slash_from_key(self):
        client = FakeS3Client()
        cloud = S3CloudStorage("gallery-backups", client=client)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            file_path.write_bytes(b"sqlite")
            key = cloud.backup_file(file_path, "/backups/artworks.db")
        self.assertEqual("backups/artworks.db", key)

    def test_backup_missing_local_file_raises_file_not_found(self):
        cloud = S3CloudStorage("gallery-backups", client=FakeS3Client())
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(FileNotFoundError):
                cloud.backup_file(Path(temp_dir) / "missing.db")

    def test_backup_directory_is_rejected(self):
        cloud = S3CloudStorage("gallery-backups", client=FakeS3Client())
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                cloud.backup_file(temp_dir)

    def test_backup_client_error_becomes_cloud_storage_error(self):
        client = FakeS3Client()
        client.upload_error = RuntimeError("network down")
        cloud = S3CloudStorage("gallery-backups", client=client)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            file_path.write_bytes(b"sqlite")
            with self.assertRaises(CloudStorageError):
                cloud.backup_file(file_path)

    def test_restore_downloads_expected_object(self):
        client = FakeS3Client()
        cloud = S3CloudStorage("gallery-backups", client=client)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            restored = cloud.restore_file(file_path, "backups/artworks.db")
            self.assertTrue(restored.exists())
            self.assertEqual(b"database content", restored.read_bytes())
        self.assertEqual("gallery-backups", client.downloads[0][0])
        self.assertEqual("backups/artworks.db", client.downloads[0][1])

    def test_restore_creates_parent_directories(self):
        cloud = S3CloudStorage("gallery-backups", client=FakeS3Client())
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "nested" / "data" / "artworks.db"
            cloud.restore_file(file_path)
            self.assertTrue(file_path.exists())

    def test_restore_client_error_becomes_cloud_storage_error(self):
        client = FakeS3Client()
        client.download_error = RuntimeError("permission denied")
        cloud = S3CloudStorage("gallery-backups", client=client)
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(CloudStorageError):
                cloud.restore_file(Path(temp_dir) / "artworks.db")

    def test_empty_object_key_is_rejected_for_backup(self):
        cloud = S3CloudStorage("gallery-backups", client=FakeS3Client())
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            file_path.write_bytes(b"sqlite")
            with self.assertRaises(ValueError):
                cloud.backup_file(file_path, "  ")

    def test_empty_object_key_is_rejected_for_restore(self):
        cloud = S3CloudStorage("gallery-backups", client=FakeS3Client())
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                cloud.restore_file(Path(temp_dir) / "artworks.db", "  ")


if __name__ == "__main__":
    unittest.main()
