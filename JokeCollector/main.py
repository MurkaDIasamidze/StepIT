"""
main.py
Joke / Quote Daily Collector — console application.

Menu-driven app that fetches jokes from JokeAPI, lets the user filter
by category, and stores/reviews/deletes previously collected jokes
in a local JSON file.
"""

from api_client import JokeAPIClient, JokeAPIError
from storage import JsonStorage, StorageError


class JokeCollectorApp:
    """Top-level application class orchestrating the CLI, API client and storage."""

    def __init__(self):
        self._api = JokeAPIClient(safe_mode=True)
        self._storage = JsonStorage("jokes_history.json")
        self._running = True

    # ---------------------------------------------------------------- menu
    def run(self):
        print("=== Joke / Quote Daily Collector ===")
        while self._running:
            self._print_menu()
            choice = input("Choose an option: ").strip()
            try:
                self._handle_choice(choice)
            except (JokeAPIError, StorageError, ValueError, IndexError) as exc:
                print(f"\n[Error] {exc}\n")
            except KeyboardInterrupt:
                print("\nInterrupted. Returning to menu...\n")

    @staticmethod
    def _print_menu():
        print(
            "\n1. Get a random joke\n"
            "2. Get a joke by category\n"
            "3. View saved jokes\n"
            "4. Filter saved jokes by category\n"
            "5. Delete a saved joke\n"
            "6. Show available categories\n"
            "7. Exit\n"
        )

    def _handle_choice(self, choice):
        actions = {
            "1": self._get_random_joke,
            "2": self._get_joke_by_category,
            "3": self._view_saved_jokes,
            "4": self._filter_saved_jokes,
            "5": self._delete_saved_joke,
            "6": self._show_categories,
            "7": self._exit_app,
        }
        action = actions.get(choice)
        if action is None:
            print("Invalid option. Please choose a number from 1 to 7.")
            return
        action()

    # ------------------------------------------------------------- actions
    def _get_random_joke(self):
        joke = self._api.fetch_joke("Any")
        print(f"\n{joke}\n")
        if self._ask_yes_no("Save this joke? (y/n): "):
            self._storage.add_joke(joke)
            print("Saved.")

    def _get_joke_by_category(self):
        categories = self._api.fetch_categories()
        print("Available categories:", ", ".join(categories))
        category = input("Enter a category: ").strip()
        if not category:
            raise ValueError("Category cannot be empty.")
        joke = self._api.fetch_joke(category)
        print(f"\n{joke}\n")
        if self._ask_yes_no("Save this joke? (y/n): "):
            self._storage.add_joke(joke)
            print("Saved.")

    def _view_saved_jokes(self):
        jokes = self._storage.get_all()
        self._print_joke_list(jokes)

    def _filter_saved_jokes(self):
        category = input("Enter category to filter by: ").strip()
        if not category:
            raise ValueError("Category cannot be empty.")
        jokes = self._storage.get_by_category(category)
        self._print_joke_list(jokes)

    def _delete_saved_joke(self):
        jokes = self._storage.get_all()
        if not self._print_joke_list(jokes):
            return
        raw_index = input("Enter the number of the joke to delete: ").strip()
        if not raw_index.isdigit():
            raise ValueError("Please enter a valid positive number.")
        removed = self._storage.delete_by_index(int(raw_index) - 1)
        print(f"Deleted: {removed}")

    def _show_categories(self):
        categories = self._api.fetch_categories()
        print("Categories:", ", ".join(categories))

    def _exit_app(self):
        print("Goodbye!")
        self._running = False

    # ------------------------------------------------------------- helpers
    @staticmethod
    def _print_joke_list(jokes):
        if not jokes:
            print("No jokes to show.")
            return False
        print()
        for i, joke in enumerate(jokes, start=1):
            print(f"{i}. {joke} (saved: {joke.created_at})")
        print()
        return True

    @staticmethod
    def _ask_yes_no(prompt):
        return input(prompt).strip().lower() in ("y", "yes")


if __name__ == "__main__":
    app = JokeCollectorApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted. Bye!")