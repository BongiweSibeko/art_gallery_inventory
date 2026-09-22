import csv
import tempfile
import unittest
from pathlib import Path

from gallery.artwork import Artwork
from gallery.inventory import GalleryInventory
from gallery.storage import FIELDNAMES, load_inventory, save_inventory


class TestStorage(unittest.TestCase):

    def make_inventory(self):
        inventory = GalleryInventory()
        inventory.add_artwork(Artwork("A001", "Sunset", "Lebo Mokoena", 5000))
        inventory.add_artwork(Artwork("A002", "City Lights", "Amahle Dube", 7500, "sold"))
        return inventory

    def test_save_inventory_creates_csv_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            self.assertTrue(file_path.exists())

    def test_save_inventory_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "data" / "nested" / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            self.assertTrue(file_path.exists())

    def test_save_inventory_writes_expected_header(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            with file_path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)
            self.assertEqual(FIELDNAMES, header)

    def test_save_inventory_writes_one_row_per_artwork(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            with file_path.open("r", newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(2, len(rows))

    def test_save_empty_inventory_writes_header_only(self):
        inventory = GalleryInventory()
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(inventory, file_path)
            with file_path.open("r", newline="", encoding="utf-8") as file:
                rows = list(csv.reader(file))
            self.assertEqual(1, len(rows))

    def test_save_inventory_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            file_path.write_text("old data", encoding="utf-8")
            save_inventory(self.make_inventory(), file_path)
            text = file_path.read_text(encoding="utf-8")
            self.assertNotIn("old data", text)

    def test_load_missing_file_returns_empty_inventory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.csv"
            inventory = load_inventory(file_path)
        self.assertEqual(0, len(inventory.artworks))

    def test_load_empty_saved_inventory_returns_empty_inventory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(GalleryInventory(), file_path)
            inventory = load_inventory(file_path)
        self.assertEqual([], inventory.artworks)

    def test_save_and_load_preserves_number_of_artworks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual(2, len(loaded.artworks))

    def test_save_and_load_preserves_artwork_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("A001", loaded.artworks[0].artwork_id)

    def test_save_and_load_preserves_title(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Sunset", loaded.find_by_id("A001").title)

    def test_save_and_load_preserves_artist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Lebo Mokoena", loaded.find_by_id("A001").artist)

    def test_save_and_load_preserves_price(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual(5000.0, loaded.find_by_id("A001").price)

    def test_save_and_load_preserves_available_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("available", loaded.find_by_id("A001").status)

    def test_save_and_load_preserves_sold_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("sold", loaded.find_by_id("A002").status)

    def test_loaded_price_is_float(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "artworks.csv"
            save_inventory(self.make_inventory(), file_path)
            loaded = load_inventory(file_path)
        self.assertIsInstance(loaded.find_by_id("A001").price, float)

    def test_unicode_text_is_saved_and_loaded(self):
        inventory = GalleryInventory()
        inventory.add_artwork(Artwork("A100", "Thabo's Résumé", "Naledi Mōkoena", 1200))
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "unicode.csv"
            save_inventory(inventory, file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Naledi Mōkoena", loaded.find_by_id("A100").artist)

    def test_commas_in_title_are_saved_and_loaded_correctly(self):
        inventory = GalleryInventory()
        inventory.add_artwork(Artwork("A101", "Sun, Moon and Stars", "Neo", 1000))
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "commas.csv"
            save_inventory(inventory, file_path)
            loaded = load_inventory(file_path)
        self.assertEqual("Sun, Moon and Stars", loaded.find_by_id("A101").title)

    def test_loading_duplicate_ids_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "duplicates.csv"
            file_path.write_text(
                "artwork_id,title,artist,price,status\n"
                "A001,One,Artist,100,available\n"
                "A001,Two,Artist,200,available\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_inventory(file_path)

    def test_loading_invalid_status_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "bad_status.csv"
            file_path.write_text(
                "artwork_id,title,artist,price,status\n"
                "A001,One,Artist,100,reserved\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_inventory(file_path)

    def test_loading_negative_price_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "bad_price.csv"
            file_path.write_text(
                "artwork_id,title,artist,price,status\n"
                "A001,One,Artist,-1,available\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_inventory(file_path)


if __name__ == "__main__":
    unittest.main()
