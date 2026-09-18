"""
storage.py
Handles persistence of jokes to a local JSON file.
"""

import json
import os

from models import Joke
from decorators import validate_non_empty


class StorageError(Exception):
    """Raised on any read/write failure against the JSON storage file."""


class JsonStorage:
    """Encapsulates reading/writing the jokes history JSON file."""

    def __init__(self, filepath="jokes_history.json"):
        self._filepath = filepath
        if not os.path.exists(self._filepath):
            self._write([])

    @property
    def filepath(self):
        return self._filepath

    def _read(self):
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as exc:
            raise StorageError(f"Storage file is corrupted: {exc}") from exc
        except OSError as exc:
            raise StorageError(f"Could not read storage file: {exc}") from exc

    def _write(self, data):
        try:
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as exc:
            raise StorageError(f"Could not write storage file: {exc}") from exc

    def add_joke(self, joke: Joke):
        data = self._read()
        data.append(joke.to_dict())
        self._write(data)

    def get_all(self):
        return [Joke.from_dict(item) for item in self._read()]

    @validate_non_empty("category")
    def get_by_category(self, category):
        category_lower = category.lower()
        return [
            Joke.from_dict(item)
            for item in self._read()
            if item.get("category", "").lower() == category_lower
        ]

    def delete_by_index(self, index):
        data = self._read()
        if index < 0 or index >= len(data):
            raise IndexError(f"No saved joke at position {index + 1}.")
        removed = data.pop(index)
        self._write(data)
        return Joke.from_dict(removed)

    def clear(self):
        self._write([])

    def count(self):
        return len(self._read())