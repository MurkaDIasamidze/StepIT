import requests
from models import Joke
from decorators import handle_api_errors

class JokeAPIService:
    BASE_URL = "https://v2.jokeapi.dev/joke"

    @handle_api_errors(retries=3, delay=1)
    def fetch_joke(self, category: str = "Any") -> Joke | None:
        """იღებს ხუმრობას JokeAPI-დან მითითებული კატეგორიით."""
        url = f"{self.BASE_URL}/{category}?safe-mode"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("error"):
            print(f"[შეცდომა] API პასუხი: {data.get('message')}")
            return None

        # ორნაწილიანი (twopart) ან ერთნაწილიანი (single) ხუმრობის დამუშავება
        if data.get("type") == "twopart":
            joke_text = f"{data.get('setup')}\n- {data.get('delivery')}"
        else:
            joke_text = data.get("joke", "")

        return Joke(
            joke_id=data.get("id", 0),
            category=data.get("category", "Any"),
            joke_type=data.get("type", "single"),
            joke_text=joke_text
        )