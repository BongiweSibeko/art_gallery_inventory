import unittest

from gallery.artwork import Artwork
from gallery.inventory import GalleryInventory


class TestGalleryInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = GalleryInventory()
        self.artwork1 = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        self.artwork2 = Artwork("A002", "City Lights", "Amahle Dube", 7500)
        self.artwork3 = Artwork("A003", "Morning Sky", "Lebo Mokoena", 2500, "sold")
        self.inventory.add_artwork(self.artwork1)
        self.inventory.add_artwork(self.artwork2)
        self.inventory.add_artwork(self.artwork3)

    def test_new_inventory_starts_empty(self):
        inventory = GalleryInventory()
        self.assertEqual([], inventory.artworks)

    def test_add_artwork_increases_inventory_size(self):
        inventory = GalleryInventory()
        inventory.add_artwork(Artwork("A010", "Ocean", "Neo", 3000))
        self.assertEqual(1, len(inventory.artworks))

    def test_add_artwork_stores_same_object(self):
        inventory = GalleryInventory()
        artwork = Artwork("A010", "Ocean", "Neo", 3000)
        inventory.add_artwork(artwork)
        self.assertIs(artwork, inventory.artworks[0])

    def test_duplicate_artwork_id_is_not_allowed(self):
        duplicate = Artwork("A001", "Other Work", "Other Artist", 1000)
        with self.assertRaises(ValueError):
            self.inventory.add_artwork(duplicate)

    def test_duplicate_id_after_trimming_is_not_allowed(self):
        duplicate = Artwork("  A001  ", "Other Work", "Other Artist", 1000)
        with self.assertRaises(ValueError):
            self.inventory.add_artwork(duplicate)

    def test_find_by_id_returns_correct_artwork(self):
        result = self.inventory.find_by_id("A002")
        self.assertIs(self.artwork2, result)

    def test_find_by_id_returns_none_when_missing(self):
        self.assertIsNone(self.inventory.find_by_id("A999"))

    def test_find_by_id_is_case_sensitive(self):
        self.assertIsNone(self.inventory.find_by_id("a001"))

    def test_find_by_id_can_find_sold_artwork(self):
        result = self.inventory.find_by_id("A003")
        self.assertEqual("sold", result.status)

    def test_search_by_artist_is_case_insensitive(self):
        results = self.inventory.search_by_artist("LEBO")
        self.assertEqual(2, len(results))

    def test_search_by_artist_finds_partial_name(self):
        results = self.inventory.search_by_artist("mok")
        self.assertEqual(2, len(results))

    def test_search_by_artist_trims_search_text(self):
        results = self.inventory.search_by_artist("  Amahle Dube  ")
        self.assertEqual(1, len(results))
        self.assertEqual("A002", results[0].artwork_id)

    def test_search_by_artist_returns_empty_list_when_no_match(self):
        results = self.inventory.search_by_artist("Unknown Artist")
        self.assertEqual([], results)

    def test_search_by_artist_can_return_sold_artwork(self):
        results = self.inventory.search_by_artist("Lebo")
        statuses = [artwork.status for artwork in results]
        self.assertIn("sold", statuses)

    def test_empty_artist_search_returns_all_artworks(self):
        results = self.inventory.search_by_artist("")
        self.assertEqual(3, len(results))

    def test_available_artworks_returns_only_available_items(self):
        results = self.inventory.available_artworks()
        self.assertEqual(2, len(results))
        self.assertTrue(all(artwork.status == "available" for artwork in results))

    def test_available_artworks_excludes_sold_items(self):
        results = self.inventory.available_artworks()
        self.assertNotIn(self.artwork3, results)

    def test_available_artworks_on_empty_inventory_returns_empty_list(self):
        inventory = GalleryInventory()
        self.assertEqual([], inventory.available_artworks())

    def test_sell_artwork_changes_status(self):
        sold = self.inventory.sell_artwork("A001")
        self.assertEqual("sold", sold.status)

    def test_sell_artwork_returns_sold_artwork(self):
        sold = self.inventory.sell_artwork("A001")
        self.assertIs(self.artwork1, sold)

    def test_sell_artwork_reduces_available_count(self):
        self.inventory.sell_artwork("A001")
        self.assertEqual(1, len(self.inventory.available_artworks()))

    def test_selling_missing_artwork_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.sell_artwork("A999")

    def test_selling_same_artwork_twice_raises_error(self):
        self.inventory.sell_artwork("A001")
        with self.assertRaises(ValueError):
            self.inventory.sell_artwork("A001")

    def test_selling_artwork_that_started_sold_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.sell_artwork("A003")

    def test_remove_artwork_returns_removed_artwork(self):
        removed = self.inventory.remove_artwork("A001")
        self.assertIs(self.artwork1, removed)

    def test_remove_artwork_reduces_inventory_size(self):
        self.inventory.remove_artwork("A001")
        self.assertEqual(2, len(self.inventory.artworks))

    def test_remove_artwork_means_it_can_no_longer_be_found(self):
        self.inventory.remove_artwork("A001")
        self.assertIsNone(self.inventory.find_by_id("A001"))

    def test_remove_sold_artwork(self):
        removed = self.inventory.remove_artwork("A003")
        self.assertEqual("sold", removed.status)

    def test_remove_missing_artwork_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_artwork("A999")

    def test_total_available_value(self):
        self.assertEqual(12500.0, self.inventory.total_available_value())

    def test_total_available_value_ignores_sold_artworks(self):
        self.assertNotEqual(15000.0, self.inventory.total_available_value())

    def test_total_available_value_changes_after_sale(self):
        self.inventory.sell_artwork("A001")
        self.assertEqual(7500.0, self.inventory.total_available_value())

    def test_total_available_value_is_zero_when_everything_is_sold(self):
        self.inventory.sell_artwork("A001")
        self.inventory.sell_artwork("A002")
        self.assertEqual(0, self.inventory.total_available_value())

    def test_total_available_value_is_zero_for_empty_inventory(self):
        inventory = GalleryInventory()
        self.assertEqual(0, inventory.total_available_value())

    def test_count_by_status_counts_available(self):
        self.assertEqual(2, self.inventory.count_by_status("available"))

    def test_count_by_status_counts_sold(self):
        self.assertEqual(1, self.inventory.count_by_status("sold"))

    def test_count_by_status_returns_zero_for_unknown_status(self):
        self.assertEqual(0, self.inventory.count_by_status("reserved"))

    def test_count_by_status_updates_after_sale(self):
        self.inventory.sell_artwork("A001")
        self.assertEqual(1, self.inventory.count_by_status("available"))
        self.assertEqual(2, self.inventory.count_by_status("sold"))

    def test_count_by_status_updates_after_removal(self):
        self.inventory.remove_artwork("A003")
        self.assertEqual(0, self.inventory.count_by_status("sold"))

    def test_inventory_preserves_artwork_order(self):
        ids = [artwork.artwork_id for artwork in self.inventory.artworks]
        self.assertEqual(["A001", "A002", "A003"], ids)


if __name__ == "__main__":
    unittest.main()
