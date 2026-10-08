
import json
import os
import uuid
from datetime import datetime


class Authentication:
    def __init__(self):
        self.file = "database/staff.json"
        self.log_file = "logs/staff.log"

        os.makedirs("database", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as file:
                json.dump([], file, indent=4)

    def generate_id(self):
        return 1000000000 + (uuid.uuid4().int % 9000000000)

    def read_data(self):
        try:
            with open(self.file, "r") as file:
                data = json.load(file)
            if not isinstance(data, list):
                return []
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def write_data(self, data):
        with open(self.file, "w") as file:
            json.dump(data, file, indent=4)

    def write_log(self, message):
        with open(self.log_file, "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def signup(self):
        print("\n========== ADD STAFF ==========")
        staff = self.read_data()
        name = input("Enter Staff Name: ").strip()

        if not name:
            print("Staff name cannot be empty.")
            return

        email = input("Enter Staff Email: ").strip().lower()

        if not email:
            print("Email cannot be empty.")
            return

        if "@" not in email or "." not in email:
            print("Invalid email.")
            return

        for user in staff:
            if user["email"] == email:
                print("Staff email already exists.")
                return

        password = input("Enter Staff Password: ").strip()

        if len(password) < 6:
            print("Password must contain at least 6 characters.")
            return

        staff_id = self.generate_id()

        while any(user["id"] == staff_id for user in staff):
            staff_id = self.generate_id()

        new_staff = {
            "id": staff_id,
            "name": name,
            "email": email,
            "password": password,
            "role": "Staff"
        }

        staff.append(new_staff)
        self.write_data(staff)
        self.write_log(f"Staff created: {staff_id} - {email}")

        print("\nStaff Account Created Successfully.")
        print(f"Staff ID: {staff_id}")
        print(f"Name: {name}")
        print(f"Email: {email}")

    def login(self):
        print("\n========== STAFF LOGIN ==========")
        email = input("Enter Email: ").strip().lower()
        password = input("Enter Password: ").strip()
        staff = self.read_data()

        for user in staff:
            if user["email"] == email and user["password"] == password:
                self.write_log(f"Staff login successful: {user['id']} - {email}")
                print("\nStaff Login Successful!")
                return user

        self.write_log(f"Staff login failed: {email}")
        print("\nInvalid Email or Password.")
        return None

    def view_staff(self):
        staff = self.read_data()

        if not staff:
            print("\nNo staff found.")
            return

        print("\n" + "=" * 100)
        print("                              STAFF LIST")
        print("=" * 100)
        print(f"{'ID':<15}{'Name':<20}{'Email':<35}{'Role':<10}")
        print("-" * 100)

        for user in staff:
            print(f"{user['id']:<15}{user['name']:<20}{user['email']:<35}{user['role']:<10}")

        print("=" * 100)

    def update_staff(self):
        staff = self.read_data()
        self.view_staff()

        if not staff:
            return

        try:
            staff_id = int(input("\nEnter Staff ID: "))
        except ValueError:
            print("Invalid Staff ID.")
            return

        selected_staff = None

        for user in staff:
            if user["id"] == staff_id:
                selected_staff = user
                break

        if selected_staff is None:
            print("Staff not found.")
            return

        name = input(f"Enter Name [{selected_staff['name']}]: ").strip()
        email = input(f"Enter Email [{selected_staff['email']}]: ").strip().lower()
        password = input("Enter New Password: ").strip()

        if name:
            selected_staff["name"] = name

        if email:
            if "@" not in email or "." not in email:
                print("Invalid email.")
                return

            for user in staff:
                if user["id"] != staff_id and user["email"] == email:
                    print("Email already exists.")
                    return

            selected_staff["email"] = email

        if password:
            if len(password) < 6:
                print("Password must contain at least 6 characters.")
                return

            selected_staff["password"] = password

        self.write_data(staff)
        self.write_log(f"Staff updated: {staff_id}")
        print("\nStaff Updated Successfully.")

    def delete_staff(self):
        staff = self.read_data()
        self.view_staff()

        if not staff:
            return

        try:
            staff_id = int(input("\nEnter Staff ID: "))
        except ValueError:
            print("Invalid Staff ID.")
            return

        selected_staff = None

        for user in staff:
            if user["id"] == staff_id:
                selected_staff = user
                break

        if selected_staff is None:
            print("Staff not found.")
            return

        staff.remove(selected_staff)
        self.write_data(staff)
        self.write_log(f"Staff deleted: {staff_id}")
        print("\nStaff Deleted Successfully.")

    def manage_staff(self):
        while True:
            print("\n========================================")
            print("             STAFF MANAGEMENT")
            print("========================================")
            print("1. Add Staff")
            print("2. View Staff")
            print("3. Update Staff")
            print("4. Delete Staff")
            print("5. Back")
            print("========================================")

            choice = input("Enter Choice: ").strip()

            if choice == "1":
                self.signup()
            elif choice == "2":
                self.view_staff()
            elif choice == "3":
                self.update_staff()
            elif choice == "4":
                self.delete_staff()
            elif choice == "5":
                break
            else:
                print("\nInvalid Choice.")
