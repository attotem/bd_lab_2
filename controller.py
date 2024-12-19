from model import Model
from view import View

class Controller:

    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            self.view.show_message("\nMenu:")
            self.view.show_message("1. View Users")
            self.view.show_message("2. Add User")
            self.view.show_message("3. Update User")
            self.view.show_message("4. Generate Users")

            self.view.show_message("")

            self.view.show_message("5. View Restaurants")
            self.view.show_message("6. Add Restaurant")
            self.view.show_message("7. Update Restaurant")
            self.view.show_message("8. Generate Restaurants")
            
            self.view.show_message("")

            self.view.show_message("9. View Restaurant Tables")
            self.view.show_message("10. Add Restaurant Table")
            self.view.show_message("11. Update Restaurant Table")
            self.view.show_message("12. Generate Restaurant Tables")

            self.view.show_message("")

            self.view.show_message("13. View Reservations")
            self.view.show_message("14. Add Reservation")
            self.view.show_message("15. Update Reservation")
            self.view.show_message("16. Generate Reservations")  # Додано пункт для генерації резервацій

            self.view.show_message("")

            self.view.show_message("17. View Contacts")
            self.view.show_message("18. Add Contact")
            self.view.show_message("19. Update Contact")
            self.view.show_message("20. Generate Contacts")
            
            self.view.show_message("")

            self.view.show_message("21. Search Data")
            self.view.show_message("22. Delete Data")
            
            self.view.show_message("")

            self.view.show_message("23. Exit")
            choice = self.view.get_input("\nEnter your choice: ")

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.add_user()
            elif choice == "3":
                self.update_user()
            elif choice == "4":
                self.generate_users()

            elif choice == "5":
                self.view_restaurants()
            elif choice == "6":
                self.add_restaurant()
            elif choice == "7":
                self.update_restaurant()
            elif choice == "8":
                self.generate_restaurants()

            elif choice == "9":
                self.view_restaurant_tables()
            elif choice == "10":
                self.add_restaurant_table()
            elif choice == "11":
                self.update_restaurant_table()
            elif choice == "12":
                self.generate_restaurant_tables()

            elif choice == "13":
                self.view_reservations()
            elif choice == "14":
                self.add_reservation()
            elif choice == "15":
                self.update_reservation()
            elif choice == "16":
                self.generate_reservations()

            elif choice == "17":
                self.view_contacts()
            elif choice == "18":
                self.add_contact()
            elif choice == "19":
                self.update_contact()
            elif choice == "20":
                self.generate_contacts()

            elif choice == "21":
                self.search_data()
            elif choice == "22":
                self.delete()
            elif choice == "23":
                self.view.show_message("Exiting...")
                break
            else:
                self.view.show_message("Invalid choice. Please try again.")

    def get_data_in_range(self):
        try:
            # Запит параметрів для отримання даних в діапазоні
            table_name = self.view.get_input("Enter the table name: ")
            id_field = self.view.get_input("Enter the ID field name: ")
            id_start = self.view.get_input("Enter the starting ID: ")
            id_end = self.view.get_input("Enter the ending ID: ")
            order_field = self.view.get_input("Enter the field to order by: ")
            
            # Формування запиту для передачі в model
            request = f"{table_name} {id_field} {id_start} {id_end} {order_field}"
            
        except Exception as e:
            self.view.show_message(f"Error in data retrieval: {str(e)}")

        return self.model.get_data_in_range(request)

    def get_data_by_field_like(self):
        try:
            # Запит параметрів для пошуку за полем
            table_name = self.view.get_input("Enter the table name: ")
            req_field = self.view.get_input("Enter the field name to search in: ")
            search_req = self.view.get_input("Enter the search text: ")
            order_field = self.view.get_input("Enter the field to order by: ")

            # Формування запиту для передачі в model
            request = f"{table_name} {req_field} {search_req} {order_field}"

        except Exception as e:
            self.view.show_message(f"Error in data retrieval: {str(e)}")

        return self.model.get_data_by_field_like(request)

    def search_data(self):
        try:
            search_type = self.view.get_input("Enter search type (1 for range, 2 for field search with LIKE): ")
            table_name = self.view.get_input("Enter table name: ")
            if table_name == 'restaurant_tables':
                table_name = 'RestaurantTables'
            else:
                table_name = table_name.capitalize()
            if search_type == '1':
                id_field = self.view.get_input("Enter the ID field to filter by (e.g., 'id' or 'order_id'): ")
                id_start = self.view.get_input("Enter the start ID: ")
                id_end = self.view.get_input("Enter the end ID: ")
                order_field = self.view.get_input("Enter the field to order by: ")
                result = self.model.get_data_in_range(table_name, id_field, id_start, id_end, order_field)
            elif search_type == '2':
                req_field = self.view.get_input("Enter the field to search (e.g., 'name' or 'status'): ")
                search_req = self.view.get_input("Enter the search term: ")
                order_field = self.view.get_input("Enter the field to order by: ")
                result = self.model.get_data_by_field_like(table_name, req_field, search_req, order_field)
            # Виведення результату
            if table_name == "Users":
                self.view.display_users(result)
            elif table_name == "Restaurants":
                self.view.display_restaurants(result)
            elif table_name == "RestaurantTables":
                self.view.show_restaurant_tables(result)
            elif table_name == "Reservations":
                self.view.show_reservations(result)
            elif table_name == "Contacts":
                self.view.show_contacts(result)
            else:
                self.view.show_message("No data found.")

        except Exception as e:
            self.view.show_message(f"An error occurred during search: {e}")

    def delete(self):
        name = self.view.get_input("Enter table name: ")
        field = self.view.get_input("Enter field name (to delete by): ")
        value = self.view.get_input("Enter field value: ")
        self.model.delete_data(name, field, value)

    def view_users(self):
        start_row = self.view.get_input("Enter start row to display from: ")
        num_rows = self.view.get_input("Enter quantity of rows to display: ")
        users = self.model.display_table_rows('Users', start_row, num_rows)
        self.view.display_users(users)

    def add_user(self):
        name = self.view.get_input("Enter the name of the user: ")
        self.model.add_user(name)

    def update_user(self):
        user_id = self.view.get_input("Enter the ID of the user to update: ")
        new_name = self.view.get_input("Enter the new name: ")
        self.model.update_user(user_id, new_name)

    def generate_users(self):
        num_users = int(self.view.get_input("Enter the number of users to generate: "))
        self.model.generate_users(num_users)

    def view_restaurants(self):
        start_row = self.view.get_input("Enter start row to display from: ")
        num_rows = self.view.get_input("Enter quantity of rows to display: ")
        restaurants = self.model.display_table_rows('Restaurants', start_row, num_rows)
        self.view.display_restaurants(restaurants)

    def add_restaurant(self):
        """Отримує дані для додавання ресторану від користувача"""
        name = self.view.get_input("Enter the restaurant name: ")
        table_quantity = self.view.get_input("Enter the number of tables: ")
        self.model.add_restaurant(name, table_quantity)

    def update_restaurant(self):
        """Отримує дані для оновлення ресторану від користувача"""
        restaurant_id = int(self.view.get_input("Enter the restaurant ID to update: "))
        name = self.view.get_input("Enter the new restaurant name: ")
        table_quantity = int(self.view.get_input("Enter the new number of tables: "))
        self.model.update_restaurant(restaurant_id, name, table_quantity)

    def generate_restaurants(self):
        num_restaurants = int(self.view.get_input("Enter the number of restaurants to generate: "))
        self.model.generate_restaurants(num_restaurants)

    def view_restaurant_tables(self):
        start_row = self.view.get_input("Enter start row to display from: ")
        num_rows = self.view.get_input("Enter quantity of rows to display: ")
        restaurant_tables = self.model.display_table_rows('RestaurantTables', start_row, num_rows)
        self.view.show_restaurant_tables(restaurant_tables)

    def add_restaurant_table(self):
        """Отримує дані для додавання таблиці ресторану від користувача"""
        capacity = int(self.view.get_input("Enter the table capacity: "))
        restaurant_id = int(self.view.get_input("Enter the restaurant ID: "))
        self.model.add_restaurant_table(capacity, restaurant_id)

    def update_restaurant_table(self):
        """Отримує дані для оновлення таблиці ресторану від користувача"""
        table_id = int(self.view.get_input("Enter the table ID to update: "))
        capacity = int(self.view.get_input("Enter the new table capacity: "))
        restaurant_id = int(self.view.get_input("Enter the new restaurant ID: "))
        self.model.update_restaurant_table(table_id, capacity, restaurant_id)

    def generate_restaurant_tables(self):
        """Генерація таблиць ресторану"""
        num_tables = int(self.view.get_input("Enter the number of tables to generate: "))
        self.model.generate_restaurant_tables(num_tables)

    def view_reservations(self):
        start_row = self.view.get_input("Enter start row to display from: ")
        num_rows = self.view.get_input("Enter quantity of rows to display: ")
        reservations = self.model.display_table_rows('Reservations', start_row, num_rows)
        self.view.show_reservations(reservations)

    def add_reservation(self):
        """Отримуємо дані для додавання бронювання"""
        user_id = int(self.view.get_input("Enter user ID: "))
        table_id = int(self.view.get_input("Enter table ID: "))
        reservation_date = self.view.get_input("Enter reservation date (YYYY-MM-DD HH:MM:SS): ")
        duration = int(self.view.get_input("Enter duration in minutes: "))
        self.model.add_reservation(user_id, table_id, reservation_date, duration)

    def update_reservation(self):
        """Отримуємо дані для оновлення бронювання"""
        reservation_id = int(self.view.get_input("Enter reservation ID to update: "))
        user_id = int(self.view.get_input("Enter new user ID: "))
        table_id = int(self.view.get_input("Enter new table ID: "))
        reservation_date = self.view.get_input("Enter new reservation date (YYYY-MM-DD HH:MM:SS): ")
        duration = int(self.view.get_input("Enter new duration in minutes: "))
        self.model.update_reservation(reservation_id, user_id, table_id, reservation_date, duration)

    def generate_reservations(self):
        """Генерація випадкових бронювань"""
        num_reservations = int(self.view.get_input("Enter number of reservations to generate: "))
        self.model.generate_reservations(num_reservations)

    def view_contacts(self):
        start_row = self.view.get_input("Enter start row to display from: ")
        num_rows = self.view.get_input("Enter quantity of rows to display: ")
        contacts = self.model.display_table_rows('Contacts', start_row, num_rows)
        self.view.show_contacts(contacts)

    def add_contact(self):
        """Отримуємо дані для додавання контакту від користувача"""
        email = self.view.get_input("Enter contact's email: ")
        phone = self.view.get_input("Enter contact's phone number: ")
        user_id = self.view.get_input("Enter user ID: ")
        
        # Перевірка на наявність унікальності email та phone
        self.model.add_contact(user_id, email, phone)
   
    def update_contact(self):
        """Оновлення даних контакту"""
        contact_id = self.view.get_input("Enter the contact ID to update: ")
        field = self.view.get_input("Enter the field name to update (email/phone/user_id): ")
        value = self.view.get_input("Enter new value: ")

        self.model.update_contact(contact_id, field, value)

    def generate_contacts(self):
        """Генерація випадкових контактів"""
        num_contacts = int(self.view.get_input("Enter number of contacts to generate: "))
        self.model.generate_contacts(num_contacts)



