import unittest

from gallery.artwork import Artwork


class TestArtwork(unittest.TestCase):

    def test_artwork_is_available_by_default(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        self.assertTrue(artwork.is_available())

    def test_default_status_is_available(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        self.assertEqual("available", artwork.status)

    def test_artwork_can_start_as_sold(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000, "sold")
        self.assertEqual("sold", artwork.status)

    def test_sold_artwork_is_not_available(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000, "sold")
        self.assertFalse(artwork.is_available())

    def test_mark_as_sold_changes_status(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        artwork.mark_as_sold()
        self.assertEqual("sold", artwork.status)

    def test_mark_as_sold_makes_artwork_unavailable(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        artwork.mark_as_sold()
        self.assertFalse(artwork.is_available())

    def test_mark_as_sold_twice_keeps_status_sold(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        artwork.mark_as_sold()
        artwork.mark_as_sold()
        self.assertEqual("sold", artwork.status)

    def test_negative_price_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("A001", "Sunset", "Lebo Mokoena", -10)

    def test_zero_price_is_allowed(self):
        artwork = Artwork("A001", "Donation", "Lebo Mokoena", 0)
        self.assertEqual(0.0, artwork.price)

    def test_integer_price_is_converted_to_float(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        self.assertIsInstance(artwork.price, float)

    def test_numeric_string_price_is_converted_to_float(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", "5000")
        self.assertEqual(5000.0, artwork.price)

    def test_invalid_price_text_raises_value_error(self):
        with self.assertRaises(ValueError):
            Artwork("A001", "Sunset", "Lebo Mokoena", "expensive")

    def test_empty_artwork_id_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("", "Sunset", "Lebo Mokoena", 5000)

    def test_whitespace_only_artwork_id_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("   ", "Sunset", "Lebo Mokoena", 5000)

    def test_empty_title_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("A001", "", "Lebo Mokoena", 5000)

    def test_whitespace_only_title_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("A001", "   ", "Lebo Mokoena", 5000)

    def test_empty_artist_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("A001", "Sunset", "", 5000)

    def test_whitespace_only_artist_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("A001", "Sunset", "   ", 5000)

    def test_invalid_status_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Artwork("A001", "Sunset", "Lebo Mokoena", 5000, "reserved")

    def test_artwork_id_whitespace_is_removed(self):
        artwork = Artwork("  A001  ", "Sunset", "Lebo Mokoena", 5000)
        self.assertEqual("A001", artwork.artwork_id)

    def test_title_whitespace_is_removed(self):
        artwork = Artwork("A001", "  Sunset  ", "Lebo Mokoena", 5000)
        self.assertEqual("Sunset", artwork.title)

    def test_artist_whitespace_is_removed(self):
        artwork = Artwork("A001", "Sunset", "  Lebo Mokoena  ", 5000)
        self.assertEqual("Lebo Mokoena", artwork.artist)

    def test_to_dict_contains_all_expected_keys(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        result = artwork.to_dict()
        self.assertEqual(
            {"artwork_id", "title", "artist", "price", "status"},
            set(result.keys()),
        )

    def test_to_dict_contains_correct_values(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        result = artwork.to_dict()
        self.assertEqual("A001", result["artwork_id"])
        self.assertEqual("Sunset", result["title"])
        self.assertEqual("Lebo Mokoena", result["artist"])
        self.assertEqual(5000.0, result["price"])
        self.assertEqual("available", result["status"])

    def test_to_dict_reflects_sold_status(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        artwork.mark_as_sold()
        self.assertEqual("sold", artwork.to_dict()["status"])

    def test_string_representation_contains_main_details(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        text = str(artwork)
        self.assertIn("A001", text)
        self.assertIn("Sunset", text)
        self.assertIn("Lebo Mokoena", text)
        self.assertIn("available", text)

    def test_string_representation_formats_price(self):
        artwork = Artwork("A001", "Sunset", "Lebo Mokoena", 5000)
        self.assertIn("R5,000.00", str(artwork))


if __name__ == "__main__":
    unittest.main()
