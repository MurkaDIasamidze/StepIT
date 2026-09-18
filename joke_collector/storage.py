import json
import os
from typing import List
from models import Joke

class StorageManager:
    def __init__(self, filename: str = "jokes_history.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            self.save_all([])

    def load_jokes(self) -> List[Joke]:
        """ტვირთავს ხუმრობებს JSON ფაილიდან (Deserialization)."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Joke.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError) as e:
            print(f"[შეცდომა] ფაილის წაკითხვისას: {e}")
            return []

    def save_all(self, jokes: List[Joke]):
        """ინახავს ხუმრობებს JSON ფაილში (Serialization)."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([j.to_dict() for j in jokes], f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"[შეცდომა] ფაილის შენახვისას: {e}")

    def add_joke(self, joke: Joke) -> bool:
        jokes = self.load_jokes()
        # დუბლიკატის შემოწმება
        if any(j.joke_text == joke.joke_text for j in jokes):
            return False
        jokes.append(joke)
        self.save_all(jokes)
        return True

    def delete_joke_by_index(self, index: int) -> bool:
        jokes = self.load_jokes()
        if 0 <= index < len(jokes):
            jokes.pop(index)
            self.save_all(jokes)
            return True
        return False