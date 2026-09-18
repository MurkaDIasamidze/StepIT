"""
api_client.py
Handles all communication with JokeAPI (https://jokeapi.dev).
"""

import requests

from decorators import retry, cache_result
from models import SingleJoke, TwoPartJoke


class JokeAPIError(Exception):
    """Raised whenever JokeAPI cannot return a usable joke."""


class JokeAPIClient:
    """Thin OOP wrapper around the JokeAPI HTTP endpoints."""

    BASE_URL = "https://v2.jokeapi.dev"

    def __init__(self, safe_mode=True, timeout=10):
        self._safe_mode = safe_mode
        self._timeout = timeout

    @property
    def safe_mode(self):
        return self._safe_mode

    @safe_mode.setter
    def safe_mode(self, value):
        self._safe_mode = bool(value)

    @retry(times=3, delay=1, exceptions=(requests.exceptions.RequestException,))
    def _get(self, url, params):
        response = requests.get(url, params=params, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def fetch_joke(self, category="Any"):
        """Fetch a single random joke, optionally filtered by category."""
        params = {}
        if self._safe_mode:
            params["safe-mode"] = ""

        url = f"{self.BASE_URL}/joke/{category}"
        try:
            data = self._get(url, params)
        except requests.exceptions.RequestException as exc:
            raise JokeAPIError(f"Could not reach JokeAPI: {exc}") from exc

        if data.get("error"):
            raise JokeAPIError(data.get("message", "JokeAPI returned an error."))

        return self._parse_joke(data)

    @cache_result
    def fetch_categories(self):
        """Fetch the list of valid categories (cached after first call)."""
        url = f"{self.BASE_URL}/categories"
        try:
            data = self._get(url, {})
        except requests.exceptions.RequestException as exc:
            raise JokeAPIError(f"Could not reach JokeAPI: {exc}") from exc
        return data.get("categories", [])

    @staticmethod
    def _parse_joke(data):
        category = data.get("category", "Unknown")
        if data.get("type") == "single":
            return SingleJoke(category=category, content=data.get("joke", ""))
        return TwoPartJoke(
            category=category,
            setup=data.get("setup", ""),
            delivery=data.get("delivery", ""),
        )