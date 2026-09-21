"""Simple inventory logic for the art gallery."""


class GalleryInventory:
    """Stores artworks and provides basic inventory operations."""

    def __init__(self):
        self.artworks = []

    def add_artwork(self, artwork):
        """Add an artwork if its ID is not already in the inventory."""
        if self.find_by_id(artwork.artwork_id) is not None:
            raise ValueError(f"Artwork ID {artwork.artwork_id} already exists")
        self.artworks.append(artwork)

    def find_by_id(self, artwork_id):
        """Find one artwork by ID. Return None when it is not found."""
        for artwork in self.artworks:
            if artwork.artwork_id == artwork_id:
                return artwork
        return None

    def search_by_artist(self, artist_name):
        """Return artworks whose artist name contains the search text."""
        search_text = artist_name.strip().lower()
        return [
            artwork
            for artwork in self.artworks
            if search_text in artwork.artist.lower()
        ]

    def available_artworks(self):
        """Return only artworks that have not been sold."""
        return [artwork for artwork in self.artworks if artwork.is_available()]

    def sell_artwork(self, artwork_id):
        """Mark an artwork as sold."""
        artwork = self.find_by_id(artwork_id)
        if artwork is None:
            raise ValueError(f"Artwork ID {artwork_id} was not found")
        if not artwork.is_available():
            raise ValueError("Artwork is already sold")

        artwork.mark_as_sold()
        return artwork

    def remove_artwork(self, artwork_id):
        """Remove an artwork and return it."""
        artwork = self.find_by_id(artwork_id)
        if artwork is None:
            raise ValueError(f"Artwork ID {artwork_id} was not found")

        self.artworks.remove(artwork)
        return artwork

    def total_available_value(self):
        """Calculate the value of all artworks that are still available."""
        return sum(artwork.price for artwork in self.available_artworks())

    def count_by_status(self, status):
        """Count how many artworks have a specific status."""
        return sum(1 for artwork in self.artworks if artwork.status == status)
