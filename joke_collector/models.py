class Joke:
    def __init__(self, joke_id: int, category: str, joke_type: str, joke_text: str):
        self.__joke_id = joke_id
        self.__category = category
        self.__joke_type = joke_type
        self.__joke_text = joke_text

    @property
    def joke_id(self):
        return self.__joke_id

    @property
    def category(self):
        return self.__category

    @property
    def joke_text(self):
        return self.__joke_text

    def to_dict(self) -> dict:
        """სერიალიზაცია JSON-ისთვის."""
        return {
            "id": self.__joke_id,
            "category": self.__category,
            "type": self.__joke_type,
            "joke": self.__joke_text
        }

    @classmethod
    def from_dict(cls, data: dict):
        """დესერიალიზაცია JSON-იდან."""
        return cls(
            joke_id=data.get("id", 0),
            category=data.get("category", "General"),
            joke_type=data.get("type", "single"),
            joke_text=data.get("joke", "")
        )

    def __str__(self):
        return f"[{self.__category}] {self.__joke_text}"