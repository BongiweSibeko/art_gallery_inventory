"""Artwork model used by the inventory tracker."""


class Artwork:
    """Represents one artwork in the gallery."""

    VALID_STATUSES = {"available", "sold"}

    def __init__(self, artwork_id, title, artist, price, status="available"):
        if not artwork_id.strip():
            raise ValueError("Artwork ID cannot be empty")
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if not artist.strip():
            raise ValueError("Artist cannot be empty")
        if float(price) < 0:
            raise ValueError("Price cannot be negative")
        if status not in self.VALID_STATUSES:
            raise ValueError("Status must be 'available' or 'sold'")

        self.artwork_id = artwork_id.strip()
        self.title = title.strip()
        self.artist = artist.strip()
        self.price = float(price)
        self.status = status

    def mark_as_sold(self):
        """Change the artwork status to sold."""
        self.status = "sold"

    def is_available(self):
        """Return True when the artwork can still be sold."""
        return self.status == "available"

    def to_dict(self):
        """Return artwork data in a dictionary for CSV storage."""
        return {
            "artwork_id": self.artwork_id,
            "title": self.title,
            "artist": self.artist,
            "price": self.price,
            "status": self.status,
        }

    def __str__(self):
        return (
            f"{self.artwork_id} | {self.title} | {self.artist} | "
            f"R{self.price:,.2f} | {self.status}"
        )
