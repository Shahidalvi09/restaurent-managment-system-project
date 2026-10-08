
import json
import os
from datetime import datetime


class TableBooking:
    def __init__(self):
        self.file = "database/tables.json"
        self.log_file = "logs/table.log"
        os.makedirs("database", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file):
            self.create_tables()
        else:
            tables = self.read_data()
            if not tables:
                self.create_tables()

    def create_tables(self):
        tables = []

        for i in range(1, 4):
            
            tables.append({
                "table_id": i,
                "table_number": f"VIP-{i}",
                "category": "VIP",
                "capacity": 8,
                "status": "Available",
                "customer_name": "",
                "customer_phone": "",
                "date": "",
                "time": "",
                "booked_at": ""
            })

        for i in range(1, 6):
            tables.append({
                "table_id": i + 3,
                "table_number": f"MED-{i}",
                "category": "Medium",
                "capacity": 6,
                "status": "Available",
                "customer_name": "",
                "customer_phone": "",
                "date": "",
                "time": "",
                "booked_at": ""
            })

        for i in range(1, 8):
            tables.append({
                "table_id": i + 8,
                "table_number": f"SML-{i}",
                "category": "Small",
                "capacity": 4,
                "status": "Available",
                "customer_name": "",
                "customer_phone": "",
                "date": "",
                "time": "",
                "booked_at": ""
            })

        self.write_data(tables)

    def read_data(self):
        try:
            with open(self.file, "r") as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def write_data(self, data):
        with open(self.file, "w") as file:
            json.dump(data, file, indent=4)

    def write_log(self, message):
        with open(self.log_file, "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def get_next_table_id(self, tables):
        if not tables:
            return 1
        return max(table.get("table_id", 0) for table in tables) + 1

    def get_table_prefix(self, category):
        if category == "VIP":
            return "VIP"
        if category == "Medium":
            return "MED"
        return "SML"

    def get_next_table_number(self, tables, category):
        prefix = self.get_table_prefix(category)
        numbers = []

        for table in tables:
            table_number = table.get("table_number", "")
            if table_number.startswith(prefix + "-"):
                try:
                    number = int(table_number.split("-")[1])
                    numbers.append(number)
                except (ValueError, IndexError):
                    pass

        next_number = max(numbers) + 1 if numbers else 1
        return f"{prefix}-{next_number}"

    def add_table(self):
        tables = self.read_data()
        print("\n========== ADD NEW TABLE ==========")
        print("1. VIP")
        print("2. Medium")
        print("3. Small")
        choice = input("Enter Category: ").strip()

        if choice == "1":
            category = "VIP"
            default_capacity = 8
        elif choice == "2":
            category = "Medium"
            default_capacity = 6
        elif choice == "3":
            category = "Small"
            default_capacity = 4
        else:
            print("Invalid category.")
            return

        capacity_input = input(f"Enter Capacity [{default_capacity}]: ").strip()
        if capacity_input:
            if not capacity_input.isdigit():
                print("Capacity must be a number.")
                return
            capacity = int(capacity_input)
            if capacity <= 0:
                print("Capacity must be greater than 0.")
                return
        else:
            capacity = default_capacity

        table_id = self.get_next_table_id(tables)
        table_number = self.get_next_table_number(tables, category)

        new_table = {
            "table_id": table_id,
            "table_number": table_number,
            "category": category,
            "capacity": capacity,
            "status": "Available",
            "customer_name": "",
            "customer_phone": "",
            "date": "",
            "time": "",
            "booked_at": ""
        }
        tables.append(new_table)
        self.write_data(tables)
        self.write_log(f"New table added: {table_number}")

        print("\nTable Added Successfully.")
        print(f"Table ID: {table_id}")
        print(f"Table Number: {table_number}")
        print(f"Category: {category}")
        print(f"Capacity: {capacity}")

    def view_tables(self):
        tables = self.read_data()
        if not tables:
            print("\nNo tables found.")
            return

        print("\n" + "=" * 110)
        print("                           RESTAURANT TABLES")
        print("=" * 110)
        print(f"{'ID':<6}{'Table':<12}{'Category':<12}{'Capacity':<12}{'Status':<15}{'Customer':<20}{'Date':<15}{'Time':<10}")
        print("-" * 110)

        for table in tables:
            print(
                f"{table.get('table_id', 'N/A'):<6}"
                f"{table.get('table_number', 'N/A'):<12}"
                f"{table.get('category', 'N/A'):<12}"
                f"{table.get('capacity', 0):<12}"
                f"{table.get('status', 'Available'):<15}"
                f"{table.get('customer_name', ''):<20}"
                f"{table.get('date', ''):<15}"
                f"{table.get('time', ''):<10}"
            )

        print("=" * 110)

    def show_available_tables(self):
        tables = self.read_data()
        available = [table for table in tables if table.get("status") == "Available"]

        if not available:
            print("\nNo tables available.")
            return

        print("\n========== AVAILABLE TABLES ==========")
        for table in available:
            print(
                f"ID: {table.get('table_id')} | "
                f"Table: {table.get('table_number')} | "
                f"Category: {table.get('category')} | "
                f"Capacity: {table.get('capacity')}"
            )

    def validate_datetime(self, date, time):
        try:
            booking_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("\nInvalid date or time.")
            print("Date format: YYYY-MM-DD")
            print("Time format: HH:MM")
            return None

        if booking_datetime <= datetime.now():
            print("\nBooking date and time must be in the future.")
            return None

        return booking_datetime

    def book_table(self):
        tables = self.read_data()
        if not tables:
            print("\nNo tables found.")
            return

        self.show_available_tables()
        available = [table for table in tables if table.get("status") == "Available"]
        if not available:
            return

        try:
            table_id = int(input("\nEnter Table ID: ").strip())
        except ValueError:
            print("Invalid Table ID.")
            return

        selected_table = None
        for table in tables:
            if table.get("table_id") == table_id:
                selected_table = table
                break

        if selected_table is None:
            print("Table not found.")
            return

        if selected_table.get("status") != "Available":
            print("This table is already booked.")
            return

        customer_name = input("Enter Customer Name: ").strip()
        if not customer_name:
            print("Customer name cannot be empty.")
            return

        customer_phone = input("Enter Customer Phone: ").strip()
        if not customer_phone.isdigit():
            print("Phone number must contain only numbers.")
            return

        if len(customer_phone) != 10:
            print("Enter a valid 10 digit phone number.")
            return

        date = input("Enter Booking Date (YYYY-MM-DD): ").strip()
        time = input("Enter Booking Time (HH:MM): ").strip()
        booking_datetime = self.validate_datetime(date, time)

        if booking_datetime is None:
            return

        selected_table["status"] = "Booked"
        selected_table["customer_name"] = customer_name
        selected_table["customer_phone"] = customer_phone
        selected_table["date"] = date
        selected_table["time"] = time
        selected_table["booked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.write_data(tables)
        self.write_log(f"Table {selected_table['table_number']} booked by {customer_name}")

        print("\n" + "=" * 45)
        print("       TABLE BOOKED SUCCESSFULLY")
        print("=" * 45)
        print(f"Table ID     : {selected_table['table_id']}")
        print(f"Table Number : {selected_table['table_number']}")
        print(f"Category     : {selected_table['category']}")
        print(f"Capacity     : {selected_table['capacity']}")
        print(f"Customer     : {customer_name}")
        print(f"Phone        : {customer_phone}")
        print(f"Date         : {date}")
        print(f"Time         : {time}")
        print("=" * 45)

    def cancel_booking(self):
        tables = self.read_data()
        if not tables:
            print("\nNo tables found.")
            return

        self.view_tables()
        try:
            table_id = int(input("\nEnter Table ID to cancel: ").strip())
        except ValueError:
            print("Invalid Table ID.")
            return

        selected_table = None
        for table in tables:
            if table.get("table_id") == table_id:
                selected_table = table
                break

        if selected_table is None:
            print("Table not found.")
            return

        if selected_table.get("status") != "Booked":
            print("This table is not booked.")
            return

        selected_table["status"] = "Available"
        selected_table["customer_name"] = ""
        selected_table["customer_phone"] = ""
        selected_table["date"] = ""
        selected_table["time"] = ""
        selected_table["booked_at"] = ""

        self.write_data(tables)
        self.write_log(f"Booking cancelled for table {selected_table['table_number']}")
        print("\nBooking Cancelled Successfully.")

    def update_booking(self):
        tables = self.read_data()
        if not tables:
            print("\nNo tables found.")
            
            return

        self.view_tables()
        try:
            table_id = int(input("\nEnter Table ID to update: ").strip())
        except ValueError:
            print("Invalid Table ID.")
            return

        selected_table = None
        for table in tables:
            if table.get("table_id") == table_id:
                selected_table = table
                break

        if selected_table is None:
            print("Table not found.")
            return

        if selected_table.get("status") != "Booked":
            print("This table is not booked.")
            return

        customer_name = input(f"Enter Customer Name [{selected_table.get('customer_name')}]: ").strip()
        customer_phone = input(f"Enter Customer Phone [{selected_table.get('customer_phone')}]: ").strip()
        date = input(f"Enter Booking Date [{selected_table.get('date')}]: ").strip()
        time = input(f"Enter Booking Time [{selected_table.get('time')}]: ").strip()

        if customer_name:
            selected_table["customer_name"] = customer_name

        if customer_phone:
            if not customer_phone.isdigit():
                print("Invalid phone number.")
                return
            if len(customer_phone) != 10:
                print("Phone number must be 10 digits.")
                return
            selected_table["customer_phone"] = customer_phone

        new_date = date if date else selected_table.get("date")
        new_time = time if time else selected_table.get("time")

        if date or time:
            booking_datetime = self.validate_datetime(new_date, new_time)
            if booking_datetime is None:
                return
            selected_table["date"] = new_date
            selected_table["time"] = new_time

        self.write_data(tables)
        self.write_log(f"Booking updated for table {selected_table['table_number']}")
        print("\nBooking Updated Successfully.")

    def delete_table(self):
        tables = self.read_data()
        if not tables:
            print("\nNo tables found.")
            return

        self.view_tables()
        try:
            table_id = int(input("\nEnter Table ID to delete: ").strip())
        except ValueError:
            print("Invalid Table ID.")
            return

        selected_table = None
        for table in tables:
            if table.get("table_id") == table_id:
                selected_table = table
                break

        if selected_table is None:
            print("Table not found.")
            return

        if selected_table.get("status") == "Booked":
            print("Booked table cannot be deleted.")
            return

        confirm = input(f"Delete {selected_table['table_number']}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Delete cancelled.")
            return

        tables.remove(selected_table)
        self.write_data(tables)
        self.write_log(f"Table deleted: {selected_table['table_number']}")
        print("\nTable Deleted Successfully.")

    def admin_table_menu(self):
        while True:
            print("\n" + "=" * 45)
            print("          ADMIN TABLE MANAGEMENT")
            print("=" * 45)
            print("1. View All Tables")
            print("2. View Available Tables")
            print("3. Add Table")
            print("4. Book Table")
            print("5. Update Booking")
            print("6. Cancel Booking")
            print("7. Delete Table")
            print("8. Back")
            print("=" * 45)

            choice = input("\nEnter Choice: ").strip()
            if choice == "1":
                self.view_tables()
            elif choice == "2":
                self.show_available_tables()
            elif choice == "3":
                self.add_table()
            elif choice == "4":
                self.book_table()
            elif choice == "5":
                self.update_booking()
            elif choice == "6":
                self.cancel_booking()
            elif choice == "7":
                self.delete_table()
            elif choice == "8":
                break
            else:
                print("Invalid Choice.")

    def staff_table_menu(self):
        while True:
            print("\n" + "=" * 45)
            print("          STAFF TABLE MANAGEMENT")
            print("=" * 45)
            print("1. View All Tables")
            print("2. View Available Tables")
            print("3. Book Table")
            print("4. Update Booking")
            print("5. Cancel Booking")
            print("6. Back")
            print("=" * 45)

            choice = input("\nEnter Choice: ").strip()
            if choice == "1":
                self.view_tables()
            elif choice == "2":
                self.show_available_tables()
            elif choice == "3":
                self.book_table()
            elif choice == "4":
                self.update_booking()
            elif choice == "5":
                self.cancel_booking()
            elif choice == "6":
                break
            else:
                print("Invalid Choice.")
