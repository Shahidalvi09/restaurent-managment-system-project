
import json
import os
from datetime import datetime


class Billing:
    def __init__(self):
        self.file = "database/bills.json"
        self.log_file = "logs/billing.log"

        os.makedirs("database", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as file:
                json.dump([], file, indent=4)

        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                file.write("")

    def log(self, message):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{date_time}] {message}\n")

    def read_data(self):
        try:
            with open(self.file, "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                self.log("Invalid bills data format.")
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            self.log("Bills JSON file is invalid or not found.")
            return []

    def write_data(self, data):
        with open(self.file, "w") as file:
            json.dump(data, file, indent=4)

    def generate_bill(self, order):
        self.log("Bill generation started.")
        order.view_orders()

        try:
            order_id = int(input("Enter Order ID: "))
        except ValueError:
            print("\n+--------------------------------------+")
            print("|         INVALID ORDER ID             |")
            print("+--------------------------------------+")
            self.log("Invalid Order ID entered.")
            return

        orders = order.read_data()
        selected_order = None

        for item in orders:
            if item["id"] == order_id:
                selected_order = item
                break

        if selected_order is None:
            print("\n+--------------------------------------+")
            print("|           ORDER NOT FOUND            |")
            print("+--------------------------------------+")
            self.log(f"Order not found. Order ID: {order_id}")
            return

        bills = self.read_data()

        for bill in bills:
            if bill["order_id"] == order_id:
                print("\n+--------------------------------------+")
                print("|       BILL ALREADY GENERATED         |")
                print("+--------------------------------------+")
                self.log(f"Bill already exists for Order ID: {order_id}")
                return

        customer_name = input("Enter Customer Name: ").strip()

        if not customer_name:
            print("\n+--------------------------------------+")
            print("|       CUSTOMER NAME REQUIRED         |")
            print("+--------------------------------------+")
            self.log(f"Customer name missing for Order ID: {order_id}")
            return

        try:
            subtotal = float(selected_order["total"])
        except (ValueError, TypeError):
            print("\n+--------------------------------------+")
            print("|          INVALID ORDER TOTAL         |")
            print("+--------------------------------------+")
            self.log(f"Invalid order total for Order ID: {order_id}")
            return

        tax_percentage = 5
        tax_amount = subtotal * tax_percentage / 100

        try:
            discount_percentage = float(input("Enter Discount Percentage: "))
        except ValueError:
            print("\n+--------------------------------------+")
            print("|           INVALID DISCOUNT           |")
            print("+--------------------------------------+")
            self.log(f"Invalid discount for Order ID: {order_id}")
            return

        if discount_percentage < 0 or discount_percentage > 100:
            print("\n+--------------------------------------+")
            print("|      DISCOUNT MUST BE 0 - 100%       |")
            print("+--------------------------------------+")
            self.log(
                f"Invalid discount percentage: {discount_percentage}% "
                f"for Order ID: {order_id}"
            )
            return

        discount_amount = subtotal * discount_percentage / 100
        final_amount = subtotal + tax_amount - discount_amount

        print("\n+--------------------------------------+")
        print("|          PAYMENT METHOD              |")
        print("+--------------------------------------+")
        print("|  1. Cash                             |")
        print("|  2. UPI                              |")
        print("|  3. Card                             |")
        print("+--------------------------------------+")

        payment_choice = input("Enter Choice: ").strip()
        payment_methods = {"1": "Cash", "2": "UPI", "3": "Card"}

        if payment_choice not in payment_methods:
            print("\n+--------------------------------------+")
            print("|        INVALID PAYMENT METHOD        |")
            print("+--------------------------------------+")
            self.log(f"Invalid payment method for Order ID: {order_id}")
            return

        payment_method = payment_methods[payment_choice]
        bill_id = max((bill["id"] for bill in bills), default=0) + 1
        bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        bill = {
            "id": bill_id,
            "order_id": order_id,
            "customer_name": customer_name,
            "date": bill_date,
            "subtotal": round(subtotal, 2),
            "tax_percentage": tax_percentage,
            "tax_amount": round(tax_amount, 2),
            "discount_percentage": discount_percentage,
            "discount_amount": round(discount_amount, 2),
            "final_amount": round(final_amount, 2),
            "payment_method": payment_method,
            "status": "Paid"
        }

        bills.append(bill)
        self.write_data(bills)
        self.log(
            f"Bill generated successfully. Bill ID: {bill_id}, "
            f"Order ID: {order_id}, Customer: {customer_name}, "
            f"Amount: ₹{round(final_amount, 2)}, Payment: {payment_method}"
        )

        print("\n+------------------------------------------------+")
        print("|                  FINAL BILL                    |")
        print("+------------------------------------------------+")
        print(f"| {'Bill ID':<25} | {bill_id:<20} |")
        print(f"| {'Order ID':<25} | {order_id:<20} |")
        print(f"| {'Customer':<25} | {customer_name:<20} |")
        print(f"| {'Date':<25} | {bill_date:<20} |")
        print("+--------------------------+---------------------+")
        print(f"| {'Subtotal':<25} | ₹{subtotal:<19.2f} |")
        print(f"| {'Tax (' + str(tax_percentage) + '%)':<25} | ₹{tax_amount:<19.2f} |")
        print(f"| {'Discount (' + str(discount_percentage) + '%)':<25} | ₹{discount_amount:<19.2f} |")
        print("+--------------------------+---------------------+")
        print(f"| {'FINAL AMOUNT':<25} | ₹{final_amount:<19.2f} |")
        print(f"| {'Payment Method':<25} | {payment_method:<20} |")
        print(f"| {'Status':<25} | {'Paid':<20} |")
        print("+------------------------------------------------+")

    def view_bills(self):
        bills = self.read_data()

        if not bills:
            print("\n+--------------------------------------+")
            print("|            NO BILLS FOUND            |")
            print("+--------------------------------------+")
            self.log("No bills found.")
            return

        print("\n" + "=" * 115)
        print(" " * 45 + "RESTAURANT BILLS")
        print("=" * 115)
        print(
            f"{'ID':<6}{'ORDER ID':<10}{'CUSTOMER NAME':<22}"
            f"{'SUBTOTAL':<15}{'TAX':<12}{'DISCOUNT':<15}"
            f"{'FINAL AMOUNT':<18}{'PAYMENT':<12}"
        )
        print("-" * 115)

        for bill in bills:
            customer_name = bill["customer_name"][:20]
            print(
                f"{bill['id']:<6}{bill['order_id']:<10}"
                f"{customer_name:<22}₹{bill['subtotal']:<14.2f}"
                f"₹{bill['tax_amount']:<11.2f}"
                f"₹{bill['discount_amount']:<14.2f}"
                f"₹{bill['final_amount']:<17.2f}"
                f"{bill['payment_method']:<12}"
            )

        print("=" * 115)
        self.log(f"All bills viewed. Total bills: {len(bills)}")

    def search_bill(self):
        self.log("Bill search started.")
        bills = self.read_data()

        if not bills:
            print("\n+--------------------------------------+")
            print("|           NO BILLS FOUND             |")
            print("+--------------------------------------+")
            self.log("No bills available for search.")
            return

        try:
            bill_id = int(input("Enter Bill ID: "))
        except ValueError:
            print("\n+--------------------------------------+")
            print("|           INVALID BILL ID            |")
            print("+--------------------------------------+")
            self.log("Invalid Bill ID entered.")
            return

        for bill in bills:
            if bill["id"] == bill_id:
                print("\n+------------------------------------------------+")
                print("|                 BILL DETAILS                   |")
                print("+--------------------------+---------------------+")
                print(f"| {'Bill ID':<25} | {bill['id']:<20} |")
                print(f"| {'Order ID':<25} | {bill['order_id']:<20} |")
                print(f"| {'Customer':<25} | {bill['customer_name']:<20} |")
                print(f"| {'Date':<25} | {bill['date']:<20} |")
                print("+--------------------------+---------------------+")
                print(f"| {'Subtotal':<25} | ₹{bill['subtotal']:<19.2f} |")
                print(f"| {'Tax':<25} | ₹{bill['tax_amount']:<19.2f} |")
                print(f"| {'Discount':<25} | ₹{bill['discount_amount']:<19.2f} |")
                print("+--------------------------+---------------------+")
                print(f"| {'FINAL AMOUNT':<25} | ₹{bill['final_amount']:<19.2f} |")
                print(f"| {'Payment':<25} | {bill['payment_method']:<20} |")
                print(f"| {'Status':<25} | {bill['status']:<20} |")
                print("+------------------------------------------------+")
                self.log(f"Bill searched successfully. Bill ID: {bill_id}")
                return

        print("\n+--------------------------------------+")
        print("|            BILL NOT FOUND            |")
        print("+--------------------------------------+")
        self.log(f"Bill not found. Bill ID: {bill_id}")

