
import json
import os
from datetime import datetime


class Order:
    def __init__(self):
        self.file = "database/orders.json"
        self.log_file = "logs/order.log"
        os.makedirs("database", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as file:
                json.dump([], file, indent=4)
            self.write_log("Orders JSON file created.")

    def write_log(self, message):
        try:
            with open(self.log_file, "a") as file:
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{date_time} - {message}\n")
        except Exception:
            pass

    def get_date_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def read_data(self):
        try:
            with open(self.file, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                self.write_log("ERROR: Orders JSON data is not a list.")
                return []
            return data

        except FileNotFoundError:
            self.write_log("ERROR: Orders JSON file not found.")
            with open(self.file, "w") as file:
                json.dump([], file, indent=4)
            return []

        except json.JSONDecodeError:
            self.write_log("ERROR: Orders JSON contains invalid JSON.")
            with open(self.file, "w") as file:
                json.dump([], file, indent=4)
            return []

        except Exception as error:
            self.write_log(f"ERROR: Orders data could not be read. {error}")
            return []

    def write_data(self, data):
        try:
            with open(self.file, "w") as file:
                json.dump(data, file, indent=4)
            self.write_log("Order data saved successfully.")
            return True
        except Exception as error:
            self.write_log(f"ERROR: Order data could not be saved. {error}")
            return False


    def create_order(self, menu):
        print("\n" + "=" * 100)
        print(" " * 42 + "CREATE ORDER")
        print("=" * 100)

        self.write_log("CREATE ORDER: Started.")

        if menu is None:
            print("\nMenu manager is not available.")
            return

        try:
            menu.view_menu()
            menu_data = menu.read_data()
        except Exception as error:
            print("\nUnable to load menu.")
            self.write_log(f"Menu loading error: {error}")
            return

        items = []

        if isinstance(menu_data, dict):
            for category, category_items in menu_data.items():
                if isinstance(category_items, list):
                    for item in category_items:
                        if isinstance(item, dict):
                            items.append(item)

        elif isinstance(menu_data, list):
            items = [
                item for item in menu_data
                if isinstance(item, dict)
            ]

        if not items:
            print("\nMenu is empty.")
            print("Please ask admin to add menu items.")
            self.write_log("CREATE ORDER FAILED: Menu is empty.")
            return

        try:
            item_id = int(input("\nEnter Menu Item ID: ").strip())
        except ValueError:
            print("\nPlease enter a valid Item ID.")
            return

        selected_item = None

        for item in items:
            try:
                if int(item["id"]) == item_id:
                    selected_item = item
                    break
            except (KeyError, TypeError, ValueError):
                continue

        if selected_item is None:
            print("\nMenu item not found.")
            return

        print("\nSelected Item:", selected_item["name"])
        print("1. Half - ₹{:.2f}".format(
            float(selected_item["half_price"])
        ))
        print("2. Full - ₹{:.2f}".format(
            float(selected_item["full_price"])
        ))

        size_choice = input("Enter Size: ").strip()

        if size_choice == "1":
            size = "Half"
            price = float(selected_item["half_price"])
        elif size_choice == "2":
            size = "Full"
            price = float(selected_item["full_price"])
        else:
            print("\nInvalid size choice.")
            return

        try:
            quantity = int(input("Enter Quantity: ").strip())
        except ValueError:
            print("\nQuantity must be a valid number.")
            return

        if quantity <= 0 or quantity > 100:
            print("\nQuantity must be between 1 and 100.")
            return

        total = round(price * quantity, 2)
        orders = self.read_data()

        valid_ids = []

        for order in orders:
            if isinstance(order, dict):
                try:
                    valid_ids.append(int(order["id"]))
                except (KeyError, TypeError, ValueError):
                    continue

        new_id = max(valid_ids) + 1 if valid_ids else 1
        current_date_time = self.get_date_time()

        new_order = {
            "id": new_id,
            "item_name": selected_item["name"],
            "size": size,
            "price": round(price, 2),
            "quantity": quantity,
            "total": total,
            "status": "Pending",
            "created_at": current_date_time,
            "updated_at": current_date_time
        }

        orders.append(new_order)

        if not self.write_data(orders):
            print("\nOrder could not be saved.")
            return

        print("\n" + "=" * 100)
        print(" " * 40 + "ORDER CREATED SUCCESSFULLY")
        print("=" * 100)
        print(f"Order ID     : {new_id}")
        print(f"Item Name    : {selected_item['name']}")
        print(f"Size         : {size}")
        print(f"Price        : ₹{price:.2f}")
        print(f"Quantity     : {quantity}")
        print(f"Total        : ₹{total:.2f}")
        print("Status       : Pending")
        print(f"Created At   : {current_date_time}")
        print("=" * 100)

        self.write_log(
            f"CREATE ORDER SUCCESS: ID={new_id}, "
            f"Item={selected_item['name']}, "
            f"Total={total}"
        )

    def view_orders(self):
        print("\n" + "=" * 125)
        print(" " * 50 + "RESTAURANT ORDERS")
        print("=" * 125)

        orders = self.read_data()
        if not orders:
            print("No orders found.")
            self.write_log("VIEW ORDERS: No orders found.")
            return

        print(f"{'ID':<6}{'ITEM NAME':<25}{'SIZE':<10}{'PRICE':<15}{'QUANTITY':<12}{'TOTAL':<15}{'STATUS':<15}{'CREATED AT':<22}")
        print("-" * 125)
        valid_orders = 0

        for order in orders:
            if not isinstance(order, dict):
                self.write_log("VIEW ERROR: Invalid order format.")
                continue

            try:
                order_id = int(order["id"])
                item_name = str(order["item_name"])
                size = str(order["size"])
                price = float(order["price"])
                quantity = int(order["quantity"])
                total = float(order["total"])
                status = str(order["status"])
                created_at = str(order.get("created_at", "-"))

                print(f"{order_id:<6}{item_name:<25}{size:<10}₹{price:<14.2f}{quantity:<12}₹{total:<14.2f}{status:<15}{created_at:<22}")
                valid_orders += 1
            except (KeyError, TypeError, ValueError):
                self.write_log("VIEW ERROR: Invalid order data found.")

        if valid_orders == 0:
            print("No valid orders found.")

        print("=" * 125)
        self.write_log("VIEW ORDERS SUCCESS: Orders viewed.")

    def update_order_status(self):
        print("\n" + "=" * 60)
        print(" " * 18 + "UPDATE ORDER STATUS")
        print("=" * 60)

        orders = self.read_data()
        if not orders:
            print("\nNo orders found.")
            self.write_log("UPDATE STATUS FAILED: No orders found.")
            return

        self.view_orders()

        try:
            order_id = int(input("\nEnter Order ID: ").strip())
        except ValueError:
            print("\nOrder ID must be a valid number.")
            self.write_log("UPDATE STATUS FAILED: Invalid order ID.")
            return

        if order_id <= 0:
            print("\nOrder ID must be greater than 0.")
            self.write_log("UPDATE STATUS FAILED: Invalid order ID value.")
            return

        selected_order = None
        for order in orders:
            if not isinstance(order, dict):
                continue
            try:
                current_id = int(order["id"])
            except (KeyError, TypeError, ValueError):
                continue

            if current_id == order_id:
                selected_order = order
                break

        if selected_order is None:
            print("\nOrder not found.")
            self.write_log(f"UPDATE STATUS FAILED: Order ID={order_id} not found.")
            return

        print("\nCurrent Status:", selected_order.get("status", "Unknown"))
        print("\n1. Pending")
        print("2. Preparing")
        print("3. Ready")
        print("4. Completed")
        print("5. Cancelled")
        choice = input("Enter New Status: ").strip()

        status_map = {
            "1": "Pending",
            "2": "Preparing",
            "3": "Ready",
            "4": "Completed",
            "5": "Cancelled"
        }

        if choice not in status_map:
            print("\nInvalid status choice.")
            self.write_log(f"UPDATE STATUS FAILED: Invalid choice. ID={order_id}")
            return

        new_status = status_map[choice]
        old_status = selected_order.get("status", "Unknown")

        if old_status == new_status:
            print("\nOrder already has this status.")
            self.write_log(f"UPDATE STATUS FAILED: Same status. ID={order_id}")
            return

        selected_order["status"] = new_status
        selected_order["updated_at"] = self.get_date_time()

        if self.write_data(orders):
            self.write_log(
                f"UPDATE STATUS SUCCESS: ID={order_id}, "
                f"Old Status={old_status}, New Status={new_status}"
            )
            print("\nOrder status updated successfully.")
            print("Order ID:", order_id)
            print("Old Status:", old_status)
            print("New Status:", new_status)
        else:
            print("\nOrder status could not be updated.")

    def delete_order(self):
        print("\n" + "=" * 60)
        print(" " * 22 + "DELETE ORDER")
        print("=" * 60)

        orders = self.read_data()
        if not orders:
            print("\nNo orders found.")
            self.write_log("DELETE ORDER FAILED: No orders found.")
            return

        self.view_orders()

        try:
            order_id = int(input("\nEnter Order ID: ").strip())
        except ValueError:
            print("\nOrder ID must be a valid number.")
            self.write_log("DELETE ORDER FAILED: Invalid order ID.")
            return

        if order_id <= 0:
            print("\nOrder ID must be greater than 0.")
            self.write_log("DELETE ORDER FAILED: Invalid order ID value.")
            return

        selected_order = None
        for order in orders:
            if not isinstance(order, dict):
                continue
            try:
                current_id = int(order["id"])
            except (KeyError, TypeError, ValueError):
                continue

            if current_id == order_id:
                selected_order = order
                break

        if selected_order is None:
            print("\nOrder not found.")
            self.write_log(f"DELETE ORDER FAILED: Order ID={order_id} not found.")
            return

        print("\nOrder found.")
        print("Item:", selected_order.get("item_name", "-"))
        print("Quantity:", selected_order.get("quantity", "-"))
        print("Total:", selected_order.get("total", "-"))
        print("Status:", selected_order.get("status", "-"))

        confirmation = input(
            "\nAre you sure you want to delete this order? (yes/no): "
        ).strip().lower()

        if confirmation not in ["yes", "y"]:
            print("\nDelete operation cancelled.")
            self.write_log(f"DELETE ORDER CANCELLED: ID={order_id}")
            return

        orders.remove(selected_order)
        if self.write_data(orders):
            self.write_log(f"DELETE ORDER SUCCESS: ID={order_id}")
            print("\nOrder deleted successfully.")
        else:
            print("\nOrder could not be deleted.")

    def manage_orders(self):
        while True:
            print("\n")
            print("=" * 60)
            print(" " * 20 + "MANAGE ORDERS")
            print("=" * 60)
            print("1. View Orders")
            print("2. Update Order Status")
            print("3. Delete Order")
            print("4. Back")
            print("=" * 60)

            choice = input("Enter Choice: ").strip()

            if choice == "1":
                self.view_orders()
            elif choice == "2":
                self.update_order_status()
            elif choice == "3":
                self.delete_order()
            elif choice == "4":
                self.write_log("MANAGE ORDERS: Returned to Admin Menu.")
                print("\nReturning to Admin Menu...")
                break
            else:
                print("\nInvalid choice.")
                self.write_log(f"MANAGE ORDERS FAILED: Invalid choice={choice}")

