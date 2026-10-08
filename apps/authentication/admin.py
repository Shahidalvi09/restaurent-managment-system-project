
import json
import os
import uuid
from datetime import datetime


class AdminAuthentication:
    def __init__(self):
        self.file = "database/admin.json"
        self.log_file = "logs/admin.log"

        os.makedirs("database", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file):
            admin = [
                {
                    "id": self.generate_id(),
                    "name": "Admin",
                    "email": "admin@gmail.com",
                    "password": "Admin123",
                    "role": "Admin"
                }
            ]

            with open(self.file, "w") as file:
                json.dump(admin, file, indent=4)

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

    def login(self):
        print("\n========== ADMIN LOGIN ==========")
        email = input("Enter Email: ").strip().lower()
        password = input("Enter Password: ").strip()
        admins = self.read_data()

        for admin in admins:
            if admin["email"] == email and admin["password"] == password:
                self.write_log(f"Admin login successful: {email}")
                print("\nAdmin Login Successful!")
                return admin

        self.write_log(f"Admin login failed: {email}")
        print("\nInvalid Email or Password.")
        return None

