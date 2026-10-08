
from apps.authentication.admin import AdminAuthentication
from apps.authentication.staff import Authentication
from apps.menu_menagment.menu import Menu
from apps.order_managment.order import Order
from apps.billing_managment.billing import Billing
from apps.inventory_managment.inventory import Inventory
from apps.table_managment.table import TableBooking


admin_auth = AdminAuthentication()
staff_auth = Authentication()
menu_manager = Menu()
order_manager = Order()
billing_manager = Billing()
inventory_manager = Inventory()
table_manager = TableBooking()


def admin_menu():
    while True:
        print("\n========================================")
        print("              ADMIN MENU")
        print("========================================")
        print("1. Add Menu Item")
        print("2. View Menu")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. Table Booking")
        print("6. Staff Management")
        print("7. View Orders")
        print("8. Manage Orders")
        print("9. Generate Bill")
        print("10. View Bills")
        print("11. Search Bill")
        print("12. Add Inventory Item")
        print("13. View Inventory")
        print("14. Update Inventory")
        print("15. Delete Inventory")
        print("16. Add Stock")
        print("17. Remove Stock")
        print("18. Low Stock")
        print("19. Inventory Value")
        print("20. Logout")
        print("========================================")

        choice = input("Enter Choice: ").strip()

        if choice == "":
            print("\nChoice cannot be empty.")
        elif choice == "1":
            menu_manager.add_item()
        elif choice == "2":
            menu_manager.view_menu()
        elif choice == "3":
            menu_manager.update_item()
        elif choice == "4":
            menu_manager.delete_item()
        elif choice == "5":
            table_manager.admin_table_menu()
        elif choice == "6":
            staff_auth.manage_staff()
        elif choice == "7":
            order_manager.view_orders()
        elif choice == "8":
            order_manager.manage_orders()
        elif choice == "9":
            billing_manager.generate_bill(order_manager)
        elif choice == "10":
            billing_manager.view_bills()
        elif choice == "11":
            billing_manager.search_bill()
        elif choice == "12":
            inventory_manager.add_item()
        elif choice == "13":
            inventory_manager.view_inventory()
        elif choice == "14":
            inventory_manager.update_item()
        elif choice == "15":
            inventory_manager.delete_item()
        elif choice == "16":
            inventory_manager.add_stock()
        elif choice == "17":
            inventory_manager.remove_stock()
        elif choice == "18":
            inventory_manager.low_stock()
        elif choice == "19":
            inventory_manager.inventory_value()
        elif choice == "20":
            print("\nAdmin Logout Successful.")
            break
        else:
            print("\nInvalid Choice. Please enter a number from 1 to 20.")


def staff_table_menu():
    while True:
        print("\n========================================")
        print("          STAFF TABLE MANAGEMENT")
        print("========================================")
        print("1. View All Tables")
        print("2. View Available Tables")
        print("3. Book Table")
        print("4. Update Booking")
        print("5. Cancel Booking")
        print("6. Back")
        print("========================================")

        choice = input("Enter Choice: ").strip()

        if choice == "":
            print("\nChoice cannot be empty.")
        elif choice == "1":
            table_manager.view_tables()
        elif choice == "2":
            table_manager.show_available_tables()
        elif choice == "3":
            table_manager.book_table()
        elif choice == "4":
            table_manager.update_booking()
        elif choice == "5":
            table_manager.cancel_booking()
        elif choice == "6":
            print("\nReturning to Staff Menu...")
            break
        else:
            print("\nInvalid Choice. Please enter a number from 1 to 6.")


def staff_menu():
    while True:
        print("\n========================================")
        print("              STAFF MENU")
        print("========================================")
        print("1. View Menu")
        print("2. Create Order")
        print("3. View Orders")
        print("4. Manage Orders")
        print("5. Generate Bill")
        print("6. View Bills")
        print("7. View Inventory")
        print("8. Table Booking")
        print("9. Logout")
        print("========================================")

        choice = input("Enter Choice: ").strip()

        if choice == "":
            print("\nChoice cannot be empty.")
        elif choice == "1":
            menu_manager.view_menu()
        elif choice == "2":
            order_manager.create_order(menu_manager)
        elif choice == "3":
            order_manager.view_orders()
        elif choice == "4":
            order_manager.manage_orders()
        elif choice == "5":
            billing_manager.generate_bill(order_manager)
        elif choice == "6":
            billing_manager.view_bills()
        elif choice == "7":
            inventory_manager.view_inventory()
        elif choice == "8":
            staff_table_menu()
        elif choice == "9":
            print("\nStaff Logout Successful.")
            break
        else:
            print("\nInvalid Choice. Please enter a number from 1 to 9.")


def display():
    while True:
        print("\n========================================")
        print("       RESTAURANT MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Admin Login")
        print("2. Staff Login")
        print("3. Exit")
        print("========================================")

        choice = input("Enter Choice: ").strip()

        if choice == "":
            print("\nChoice cannot be empty.")
        elif choice == "1":
            admin = admin_auth.login()
            if admin:
                admin_menu()
        elif choice == "2":
            staff = staff_auth.login()
            if staff:
                staff_menu()
        elif choice == "3":
            print("\nThank you for using Restaurant Management System.")
            break
        else:
            print("\nInvalid Choice. Please enter 1, 2 or 3.")

