
import json
import os
from datetime import datetime


class Menu:

    def __init__(self):
        self.file = "database/menu.json"
        self.log_file = "logs/menu.log"

        os.makedirs("database", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as file:
                json.dump({}, file, indent=4)

    def write_log(self, message):
        with open(self.log_file, "a") as file:
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{date_time} - {message}\n")

    def read_data(self):
        try:
            with open(self.file, "r") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                self.write_log("ERROR: Menu data must be a dictionary.")
                return {}

            return data

        except (FileNotFoundError, json.JSONDecodeError) as error:
            self.write_log(f"ERROR: Menu file could not be read. {error}")
            return {}

    def write_data(self, data):
        try:
            with open(self.file, "w") as file:
                json.dump(data, file, indent=4)

            return True

        except Exception as error:
            self.write_log(f"ERROR: Menu data could not be saved. {error}")
            return False

    def select_category(self, menu):
        categories = list(menu.keys())

        print("\n")
        print("=" * 50)
        print("              FOOD CATEGORIES")
        print("=" * 50)

        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        print("=" * 50)

        try:
            choice = int(input("Select Category: ").strip())

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Invalid category choice.")
            return None

        except ValueError:
            print("Please enter a valid number.")
            return None

    def view_menu(self):
        menu = self.read_data()

        if not menu:
            print("Menu is empty.")
            return

        print("\n")
        print("=" * 100)
        print("                         RESTAURANT MENU")
        print("=" * 100)

        for category, items in menu.items():
            print("\n")
            print("-" * 100)
            print(f"{category.upper():^100}")
            print("-" * 100)

            print(
                f"{'ID':<6}"
                f"{'ITEM NAME':<35}"
                f"{'FOOD TYPE':<15}"
                f"{'HALF PRICE':<20}"
                f"{'FULL PRICE':<15}"
            )

            print("-" * 100)

            for item in items:
                print(
                    f"{item['id']:<6}"
                    f"{item['name']:<35}"
                    f"{item['food_type']:<15}"
                    f"{item['half_price']:<20.2f}"
                    f"{item['full_price']:<15.2f}"
                )

        print("\n" + "=" * 100)
        print("                     MENU DISPLAY COMPLETED")
        print("=" * 100)

        self.write_log("VIEW SUCCESS: All menu categories displayed.")

    def add_item(self):
        menu = self.read_data()

        category = self.select_category(menu)

        if category is None:
            return

        name = input("Enter Item Name: ").strip()

        if not name:
            print("Item name cannot be empty.")
            return

        for items in menu.values():
            for item in items:
                if item["name"].strip().lower() == name.lower():
                    print("This item already exists.")
                    return

        food_type = input("Enter Food Type (veg/non veg): ").strip().lower()

        if food_type not in ["veg", "non veg"]:
            print("Food type must be veg or non veg.")
            return

        try:
            half_price = float(input("Enter Half Price: ").strip())
            full_price = float(input("Enter Full Price: ").strip())

            if half_price <= 0 or full_price <= 0:
                print("Prices must be greater than zero.")
                return

            if full_price < half_price:
                print("Full price cannot be less than half price.")
                return

        except ValueError:
            print("Please enter valid prices.")
            return

        ids = [
            item["id"]
            for items in menu.values()
            for item in items
            if isinstance(item.get("id"), int)
        ]

        new_id = max(ids, default=0) + 1

        new_item = {
            "id": new_id,
            "name": name,
            "food_type": food_type,
            "half_price": half_price,
            "full_price": full_price
        }

        menu[category].append(new_item)

        if self.write_data(menu):
            print("Menu item added successfully.")
            self.write_log(f"ADD SUCCESS: ID={new_id}, Name={name}")

    def update_item(self):
        menu = self.read_data()

        if not menu:
            print("Menu is empty.")
            return

        self.view_menu()

        try:
            item_id = int(input("\nEnter Item ID to update: ").strip())
        except ValueError:
            print("Invalid item ID.")
            return

        selected_item = None

        for items in menu.values():
            for item in items:
                if item.get("id") == item_id:
                    selected_item = item
                    break

            if selected_item:
                break

        if selected_item is None:
            print("Item not found.")
            return

        new_name = input("Enter New Name: ").strip()

        if not new_name:
            print("Name cannot be empty.")
            return

        for items in menu.values():
            for item in items:
                if item is not selected_item:
                    if item["name"].strip().lower() == new_name.lower():
                        print("This item name already exists.")
                        return

        food_type = input("Enter Food Type (veg/non veg): ").strip().lower()

        if food_type not in ["veg", "non veg"]:
            print("Invalid food type.")
            return

        try:
            half_price = float(input("Enter New Half Price: ").strip())
            full_price = float(input("Enter New Full Price: ").strip())

            if half_price <= 0 or full_price < half_price:
                print("Invalid prices.")
                return

        except ValueError:
            print("Please enter valid prices.")
            return

        selected_item["name"] = new_name
        selected_item["food_type"] = food_type
        selected_item["half_price"] = half_price
        selected_item["full_price"] = full_price

        if self.write_data(menu):
            print("Menu item updated successfully.")
            self.write_log(f"UPDATE SUCCESS: ID={item_id}")

    def delete_item(self):
        menu = self.read_data()

        if not menu:
            print("Menu is empty.")
            return

        self.view_menu()

        try:
            item_id = int(input("\nEnter Item ID to delete: ").strip())
        except ValueError:
            print("Invalid item ID.")
            return

        for category, items in menu.items():
            for item in items:
                if item.get("id") == item_id:
                    print("Item Name:", item["name"])

                    confirm = input(
                        "Are you sure you want to delete? (yes/no): "
                    ).strip().lower()

                    if confirm not in ["yes", "y"]:
                        print("Delete cancelled.")
                        return

                    items.remove(item)

                    if self.write_data(menu):
                        print("Menu item deleted successfully.")
                        self.write_log(f"DELETE SUCCESS: ID={item_id}")

                    return

        print("Item not found.")


if __name__ == "__main__":
    menu_manager = Menu()

    while True:
        print("\n")
        print("=" * 50)
        print("             RESTAURANT MENU SYSTEM")
        print("=" * 50)
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. Exit")
        print("=" * 50)

        choice = input("Enter Choice: ").strip()

        if choice == "1":
            menu_manager.view_menu()

        elif choice == "2":
            menu_manager.add_item()

        elif choice == "3":
            menu_manager.update_item()

        elif choice == "4":
            menu_manager.delete_item()

        elif choice == "5":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")