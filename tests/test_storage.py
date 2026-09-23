import sqlite3
import tempfile
import unittest
from pathlib import Path

from gallery.artwork import Artwork
from gallery.inventory import GalleryInventory
from gallery.storage import FIELDNAMES, TABLE_NAME, load_inventory, save_inventory


class TestStorage(unittest.TestCase):

    def make_inventory(self):
        inventory = GalleryInventory()
        inventory.add_artwork(Artwork("A001", "Sunset", "Lebo Mokoena", 5000))
        inventory.add_artwork(Artwork("A002", "City Lights", "Amahle Dube", 7500, "sold"))
        return inventory

    def write_raw_rows(self, file_path, rows):
        """Write rows straight into the database, bypassing save_inventory.

        Used to simulate a data file that was hand-edited or produced by
        something else, so we can test that load_inventory rejects bad data
        it did not create itself.
        """
        connection = sqlite3.connect(file_path)
        connection.execute(
            f"""
            CREATE TABLE {TABLE_NAME} (
                artwork_id TEXT NOT NULL,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                price REAL NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            f"INSERT INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?)", rows
        )
        connection.commit()
        connection.close()

    # --- saving -------------------------------------------------------------

    def test_save_inventory_creates_database_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            self.assertTrue(file_path.exists())

    def test_save_inventory_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "data" / "nested" / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            self.assertTrue(file_path.exists())

    def test_save_inventory_creates_table_with_expected_columns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            connection = sqlite3.connect(file_path)
            columns = [row[1] for row in connection.execute(
                f"PRAGMA table_info({TABLE_NAME})"
            )]
            connection.close()
            self.assertEqual(FIELDNAMES, columns)

    def test_save_inventory_writes_one_row_per_artwork(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            connection = sqlite3.connect(file_path)
            count = connection.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
            connection.close()
            self.assertEqual(2, count)

    def test_save_empty_inventory_creates_table_with_no_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(GalleryInventory(), file_path)
            connection = sqlite3.connect(file_path)
            count = connection.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
            connection.close()
            self.assertEqual(0, count)

    def test_save_inventory_replaces_previously_saved_artworks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            old_inventory = GalleryInventory()
            old_inventory.add_artwork(Artwork("OLD1", "Old Work", "Old Artist", 100))
            save_inventory(old_inventory, file_path)

            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)

        self.assertIsNone(loaded.find_by_id("OLD1"))
        self.assertIsNotNone(loaded.find_by_id("A001"))

    def test_saving_twice_does_not_duplicate_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual(2, len(loaded.artworks))

    # --- loading --------------------------------------------------------

    def test_load_missing_file_returns_empty_inventory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.db"
            inventory = load_inventory(file_path)
        self.assertEqual(0, len(inventory.artworks))

    def test_load_empty_saved_inventory_returns_empty_inventory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(GalleryInventory(), file_path)
            inventory = load_inventory(file_path)
        self.assertEqual([], inventory.artworks)

    # --- round trip: save then load should preserve everything -------------

    def test_save_and_load_preserves_number_of_artworks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual(2, len(loaded.artworks))

    def test_save_and_load_preserves_artwork_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("A001", loaded.artworks[0].artwork_id)

    def test_save_and_load_preserves_title(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Sunset", loaded.find_by_id("A001").title)

    def test_save_and_load_preserves_artist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Lebo Mokoena", loaded.find_by_id("A001").artist)

    def test_save_and_load_preserves_price(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual(5000.0, loaded.find_by_id("A001").price)

    def test_save_and_load_preserves_available_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("available", loaded.find_by_id("A001").status)

    def test_save_and_load_preserves_sold_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("sold", loaded.find_by_id("A002").status)

    def test_loaded_price_is_float(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.db"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertIsInstance(loaded.find_by_id("A001").price, float)

    def test_unicode_text_is_saved_and_loaded(self):
        inventory = GalleryInventory()
        inventory.add_artwork(Artwork("A100", "Thabo's Résumé", "Naledi Mōkoena", 1200))
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "unicode.db"
            save_inventory(inventory, file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Naledi Mōkoena", loaded.find_by_id("A100").artist)

    def test_commas_in_title_are_saved_and_loaded_correctly(self):
        inventory = GalleryInventory()
        inventory.add_artwork(Artwork("A101", "Sun, Moon and Stars", "Neo", 1000))
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "commas.db"
            save_inventory(inventory, file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Sun, Moon and Stars", loaded.find_by_id("A101").title)

    # --- loading data that did not come from save_inventory ----------------
    # These simulate a database file that was hand-edited, or written by
    # something else, so load_inventory has to defend itself the same way
    # it did against a hand-edited CSV.

    def test_loading_duplicate_ids_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "duplicates.db"
            self.write_raw_rows(file_path, [
                ("A001", "One", "Artist", 100, "available"),
                ("A001", "Two", "Artist", 200, "available"),
            ])
            with self.assertRaises(ValueError):
                load_inventory(file_path)

    def test_loading_invalid_status_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "bad_status.db"
            self.write_raw_rows(file_path, [
                ("A001", "One", "Artist", 100, "reserved"),
            ])
            with self.assertRaises(ValueError):
                load_inventory(file_path)

    def test_loading_negative_price_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "bad_price.db"
            self.write_raw_rows(file_path, [
                ("A001", "One", "Artist", -1, "available"),
            ])
            with self.assertRaises(ValueError):
                load_inventory(file_path)


if __name__ == "__main__":
    unittest.main()
