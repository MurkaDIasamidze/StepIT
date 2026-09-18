"""
models.py
Domain model for jokes, using OOP with encapsulation and inheritance.
"""

from datetime import datetime


class Joke:
    """Base class representing a single stored joke/quote entry."""

    def __init__(self, category, content, joke_type="single", created_at=None):
        self._category = category or "Unknown"
        self._content = content or ""
        self._type = joke_type
        self._created_at = created_at or datetime.now().isoformat(timespec="seconds")

    # --- Encapsulated read-only properties -----------------------------
    @property
    def category(self):
        return self._category

    @property
    def content(self):
        return self._content

    @property
    def joke_type(self):
        return self._type

    @property
    def created_at(self):
        return self._created_at

    # --- Serialization ---------------------------------------------------
    def to_dict(self):
        return {
            "category": self._category,
            "content": self._content,
            "type": self._type,
            "created_at": self._created_at,
        }

    @classmethod
    def from_dict(cls, data):
        joke_type = data.get("type", "single")
        if joke_type == "twopart":
            return TwoPartJoke.from_dict(data)
        return SingleJoke(
            category=data.get("category", "Unknown"),
            content=data.get("content", ""),
            created_at=data.get("created_at"),
        )

    def __str__(self):
        return f"[{self._category}] {self._content}"


class SingleJoke(Joke):
    """A one-liner joke."""

    def __init__(self, category, content, created_at=None):
        super().__init__(category, content, joke_type="single", created_at=created_at)


class TwoPartJoke(Joke):
    """A setup/delivery style joke. Demonstrates extended state via inheritance."""

    def __init__(self, category, setup, delivery, created_at=None):
        content = f"{setup} ... {delivery}"
        super().__init__(category, content, joke_type="twopart", created_at=created_at)
        self._setup = setup
        self._delivery = delivery

    @property
    def setup(self):
        return self._setup

    @property
    def delivery(self):
        return self._delivery

    def to_dict(self):
        data = super().to_dict()
        data["setup"] = self._setup
        data["delivery"] = self._delivery
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            category=data.get("category", "Unknown"),
            setup=data.get("setup", ""),
            delivery=data.get("delivery", ""),
            created_at=data.get("created_at"),
        )