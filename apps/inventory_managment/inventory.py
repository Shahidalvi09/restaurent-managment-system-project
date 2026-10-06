
import json
import os
from datetime import datetime


class Inventory:
    def __init__(self):
        self.file = "database/inventory.json"
        self.log_file = "logs/inventory.log"
        os.makedirs("database", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as file:
                json.dump([], file, indent=4)

    def log(self, message):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{date_time}] {message}\n")

    def read_data(self):
        try:
            with open(self.file, "r") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    self.log("Inventory JSON does not contain a list.")
                    return []
                return data
        except FileNotFoundError:
            self.log("Inventory file not found. Creating new file.")
            with open(self.file, "w") as file:
                json.dump([], file, indent=4)
            return []
        except json.JSONDecodeError:
            self.log("Inventory JSON file is corrupted.")
            print("\nInventory file is empty or corrupted.")
            return []

    def write_data(self, data):
        try:
            with open(self.file, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            self.log(f"Error writing inventory data: {e}")
            print("\nUnable to save inventory data.")
            return False

    def generate_id(self, data):
        if not data:
            return 1

        ids = []
        for item in data:
            try:
                ids.append(int(item.get("id", 0)))
            except (ValueError, TypeError):
                continue

        if not ids:
            return 1
        return max(ids) + 1

    def add_item(self):
        print("\n========== ADD INVENTORY ITEM ==========")
        name = input("Enter item name: ").strip()

        if not name:
            print("Item name cannot be empty.")
            return

        category = input("Enter category: ").strip()
        if not category:
            print("Category cannot be empty.")
            return

        unit = input("Enter unit (kg/litre/piece): ").strip()
        if not unit:
            print("Unit cannot be empty.")
            return

        try:
            quantity = float(input("Enter quantity: "))
            if quantity < 0:
                print("Quantity cannot be negative.")
                return
        except ValueError:
            print("Please enter a valid quantity.")
            return

        try:
            minimum_stock = float(input("Enter minimum stock level: "))
            if minimum_stock < 0:
                print("Minimum stock cannot be negative.")
                return
        except ValueError:
            print("Please enter a valid minimum stock.")
            return

        try:
            price = float(input("Enter price per unit: "))
            if price < 0:
                print("Price cannot be negative.")
                return
        except ValueError:
            print("Please enter a valid price.")
            return

        data = self.read_data()
        for item in data:
            old_name = str(item.get("name", "")).strip().lower()
            if old_name == name.lower():
                print("\nItem already exists.")
                self.log(f"Duplicate item attempt: {name}")
                return

        item_id = self.generate_id(data)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_item = {
            "id": item_id,
            "name": name,
            "category": category,
            "unit": unit,
            "quantity": quantity,
            "minimum_stock": minimum_stock,
            "price_per_unit": price,
            "created_at": current_time,
            "updated_at": current_time
        }

        data.append(new_item)
        if self.write_data(data):
            print("\nInventory item added successfully.")
            self.log(f"Inventory item added: ID={item_id}, Name={name}")

    def view_inventory(self):
        print("\n================ INVENTORY ================")
        data = self.read_data()

        if not data:
            print("Inventory is empty.")
            return

        print(f"{'ID':<5}{'Name':<20}{'Category':<15}{'Unit':<10}{'Qty':<10}{'Min':<10}{'Price':<12}Status")
        print("-" * 100)

        for item in data:
            quantity = float(item.get("quantity", 0))
            minimum = float(item.get("minimum_stock", 0))

            if quantity == 0:
                status = "OUT OF STOCK"
            elif quantity <= minimum:
                status = "LOW STOCK"
            else:
                status = "AVAILABLE"

            print(
                f"{str(item.get('id', 'N/A')):<5}"
                f"{str(item.get('name', 'N/A')):<20}"
                f"{str(item.get('category', 'N/A')):<15}"
                f"{str(item.get('unit', 'N/A')):<10}"
                f"{quantity:<10.2f}{minimum:<10.2f}"
                f"{float(item.get('price_per_unit', 0)):<12.2f}{status}"
            )

    def search_item(self):
        print("\n========== SEARCH INVENTORY ==========")
        search = input("Enter item name: ").strip().lower()

        if not search:
            print("Search cannot be empty.")
            return

        data = self.read_data()
        found = False

        for item in data:
            item_name = str(item.get("name", "")).lower()
            if search in item_name:
                found = True
                print("\n========== ITEM FOUND ==========")
                print("ID:", item.get("id", "N/A"))
                print("Name:", item.get("name", "N/A"))
                print("Category:", item.get("category", "N/A"))
                print("Unit:", item.get("unit", "N/A"))
                print("Quantity:", item.get("quantity", 0))
                print("Minimum Stock:", item.get("minimum_stock", 0))
                print("Price Per Unit:", item.get("price_per_unit", 0))

        if not found:
            print("\nItem not found.")

    def update_item(self):
        print("\n========== UPDATE INVENTORY ==========")

        try:
            item_id = int(input("Enter item ID: "))
        except ValueError:
            print("Please enter a valid ID.")
            return

        data = self.read_data()

        for item in data:
            if int(item.get("id", 0)) == item_id:
                print("\nLeave field empty to keep old value.")
                name = input(f"Name ({item.get('name', '')}): ").strip()
                category = input(f"Category ({item.get('category', '')}): ").strip()
                unit = input(f"Unit ({item.get('unit', '')}): ").strip()
                quantity = input(f"Quantity ({item.get('quantity', 0)}): ").strip()
                minimum = input(f"Minimum Stock ({item.get('minimum_stock', 0)}): ").strip()
                price = input(f"Price ({item.get('price_per_unit', 0)}): ").strip()

                if name:
                    for other_item in data:
                        if (
                            int(other_item.get("id", 0)) != item_id
                            and str(other_item.get("name", "")).lower() == name.lower()
                        ):
                            print("\nAnother item with this name already exists.")
                            return
                    item["name"] = name

                if category:
                    item["category"] = category
                if unit:
                    item["unit"] = unit

                if quantity:
                    try:
                        quantity_value = float(quantity)
                        if quantity_value < 0:
                            print("Quantity cannot be negative.")
                            return
                        item["quantity"] = quantity_value
                    except ValueError:
                        print("Invalid quantity.")
                        return

                if minimum:
                    try:
                        minimum_value = float(minimum)
                        if minimum_value < 0:
                            print("Minimum stock cannot be negative.")
                            return
                        item["minimum_stock"] = minimum_value
                    except ValueError:
                        print("Invalid minimum stock.")
                        return

                if price:
                    try:
                        price_value = float(price)
                        if price_value < 0:
                            print("Price cannot be negative.")
                            return
                        item["price_per_unit"] = price_value
                    except ValueError:
                        print("Invalid price.")
                        return

                item["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if self.write_data(data):
                    print("\nInventory updated successfully.")
                    self.log(f"Inventory updated: ID={item_id}")
                return

        print("\nInventory item not found.")

    def delete_item(self):
        print("\n========== DELETE INVENTORY ITEM ==========")

        try:
            item_id = int(input("Enter item ID: "))
        except ValueError:
            print("Please enter a valid ID.")
            return

        data = self.read_data()

        for item in data:
            if int(item.get("id", 0)) == item_id:
                print("\nItem:", item.get("name", "Unknown"))
                confirm = input("Are you sure? (yes/no): ").strip().lower()

                if confirm != "yes":
                    print("Delete cancelled.")
                    return

                data.remove(item)
                if self.write_data(data):
                    print("\nInventory item deleted successfully.")
                    self.log(f"Inventory item deleted: ID={item_id}")
                return

        print("\nInventory item not found.")

    def add_stock(self):
        print("\n========== ADD STOCK ==========")

        try:
            item_id = int(input("Enter item ID: "))
        except ValueError:
            print("Please enter a valid ID.")
            return

        try:
            amount = float(input("Enter stock quantity to add: "))
            if amount <= 0:
                print("Quantity must be greater than 0.")
                return
        except ValueError:
            print("Please enter a valid quantity.")
            return

        data = self.read_data()

        for item in data:
            if int(item.get("id", 0)) == item_id:
                old_quantity = float(item.get("quantity", 0))
                item["quantity"] = old_quantity + amount
                item["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if self.write_data(data):
                    print("\nStock added successfully.")
                    print("Old Quantity:", old_quantity)
                    print("New Quantity:", item["quantity"])
                    self.log(f"Stock added: ID={item_id}, Amount={amount}")
                return

        print("\nInventory item not found.")

    def remove_stock(self):
        print("\n========== REMOVE STOCK ==========")

        try:
            item_id = int(input("Enter item ID: "))
        except ValueError:
            print("Please enter a valid ID.")
            return

        try:
            amount = float(input("Enter stock quantity to remove: "))
            if amount <= 0:
                print("Quantity must be greater than 0.")
                return
        except ValueError:
            print("Please enter a valid quantity.")
            return

        data = self.read_data()

        for item in data:
            if int(item.get("id", 0)) == item_id:
                current_quantity = float(item.get("quantity", 0))

                if amount > current_quantity:
                    print("\nNot enough stock available.")
                    self.log(f"Failed stock removal: ID={item_id}, Amount={amount}")
                    return

                item["quantity"] = current_quantity - amount
                item["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if self.write_data(data):
                    print("\nStock removed successfully.")
                    print("Old Quantity:", current_quantity)
                    print("New Quantity:", item["quantity"])
                    self.log(f"Stock removed: ID={item_id}, Amount={amount}")
                return

        print("\nInventory item not found.")

    def low_stock(self):
        print("\n========== LOW STOCK ITEMS ==========")
        data = self.read_data()

        if not data:
            print("Inventory is empty.")
            return

        found = False
        for item in data:
            quantity = float(item.get("quantity", 0))
            minimum = float(item.get("minimum_stock", 0))

            if quantity <= minimum:
                found = True
                print(
                    f"ID: {item.get('id', 'N/A')} | "
                    f"Name: {item.get('name', 'N/A')} | "
                    f"Quantity: {quantity} {item.get('unit', '')} | "
                    f"Minimum: {minimum} {item.get('unit', '')}"
                )

        if not found:
            print("No low stock items.")

    def inventory_value(self):
        print("\n========== INVENTORY VALUE ==========")
        data = self.read_data()

        if not data:
            print("Inventory is empty.")
            return

        total = 0
        for item in data:
            quantity = float(item.get("quantity", 0))
            price = float(item.get("price_per_unit", 0))
            total += quantity * price

        print(f"Total Inventory Value: ₹{total:.2f}")
        self.log(f"Inventory value checked: ₹{total:.2f}")

