from api_service import JokeAPIService
from storage import StorageManager

class JokeApp:
    CATEGORIES = ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"]

    def __init__(self):
        self.api = JokeAPIService()
        self.storage = StorageManager()

    def display_menu(self):
        print("\n=== Joke Daily Collector ===")
        print("1. რენდომ ხუმრობის მიღება")
        print("2. ხუმრობის მიღება კატეგორიის მიხედვით")
        print("3. შენახული ხუმრობების ნახვა")
        print("4. ხუმრობის წაშლა ისტორიიდან")
        print("5. გამოსვლა")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nაირჩიეთ ოპერაცია (1-5): ").strip()

            if choice == "1":
                self.get_and_save_joke("Any")
            elif choice == "2":
                self.get_joke_by_category()
            elif choice == "3":
                self.view_saved_jokes()
            elif choice == "4":
                self.delete_joke()
            elif choice == "5":
                print("ნახვამდის!")
                break
            else:
                print("[შეცდომა] არასწორი არჩევანი. გთხოვთ შეიყვანოთ ციფრი 1-დან 5-მდე.")

    def get_and_save_joke(self, category: str):
        print("\nიტვირთება ხუმრობა...")
        joke = self.api.fetch_joke(category)
        if joke:
            print("\n--- მიღებული ხუმრობა ---")
            print(joke)
            print("------------------------")
            
            save = input("გსურთ ამ ხუმრობის შენახვა? (y/n): ").strip().lower()
            if save == 'y':
                if self.storage.add_joke(joke):
                    print("ხუმრობა წარმატებით შენახდა!")
                else:
                    print("ეს ხუმრობა უკვე არსებობს ისტორიაში.")

    def get_joke_by_category(self):
        print("\nხელმისაწვდომი კატეგორიები:")
        for idx, cat in enumerate(self.CATEGORIES[1:], 1):
            print(f"{idx}. {cat}")

        try:
            cat_choice = int(input("\nაირჩიეთ კატეგორიის ნომერი: "))
            if 1 <= cat_choice < len(self.CATEGORIES):
                selected_cat = self.CATEGORIES[cat_choice]
                self.get_and_save_joke(selected_cat)
            else:
                print("[შეცდომა] არასწორი კატეგორიის ნომერი.")
        except ValueError:
            print("[შეცდომა] გთხოვთ შეიყვანოთ ვალიდური ციფრი.")

    def view_saved_jokes(self):
        jokes = self.storage.load_jokes()
        if not jokes:
            print("\nშენახული ხუმრობები არ არის.")
            return

        print(f"\n=== შენახული ხუმრობები ({len(jokes)}) ===")
        for idx, joke in enumerate(jokes, 1):
            print(f"{idx}. {joke}")

    def delete_joke(self):
        jokes = self.storage.load_jokes()
        if not jokes:
            print("\nწასაშლელი ხუმრობები არ არის.")
            return

        self.view_saved_jokes()
        try:
            idx = int(input("\nშეიყვანეთ წასაშლელი ხუმრობის ნომერი: ")) - 1
            if self.storage.delete_joke_by_index(idx):
                print("ხუმრობა წარმატებით წაიშალა!")
            else:
                print("[შეცდომა] არასწორი ინდექსი.")
        except ValueError:
            print("[შეცდომა] გთხოვთ შეიყვანოთ ვალიდური ციფრი.")


if __name__ == "__main__":
    app = JokeApp()
    app.run()