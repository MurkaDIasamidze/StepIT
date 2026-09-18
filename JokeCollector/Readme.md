# Joke / Quote Daily Collector

A console application that fetches jokes from [JokeAPI](https://jokeapi.dev),
lets you browse and filter them, and saves your favorites to a local JSON file.

## Features
- Fetch random jokes or jokes filtered by category from JokeAPI.
- Save fetched jokes to `jokes_history.json`.
- View all saved jokes.
- Filter saved jokes by category.
- Delete a saved joke by number.
- List categories supported by the API (cached after the first fetch).

## Project structure
```
main.py         # CLI entry point / menu (JokeCollectorApp)
api_client.py   # JokeAPIClient: talks to JokeAPI, retry + caching decorators
storage.py      # JsonStorage: JSON-file persistence layer
models.py       # Joke / SingleJoke / TwoPartJoke classes
decorators.py   # retry, validate_non_empty, cache_result decorators
requirements.txt
```

## Setup

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Notes
- Requests to JokeAPI are wrapped in a `retry` decorator (3 attempts with a
  1-second delay) to handle transient network errors.
- The category list is cached in memory via the `cache_result` decorator so
  it isn't re-fetched on every menu action.
- All storage and API errors are caught in `main.py` and shown as clear
  messages instead of crashing the app.