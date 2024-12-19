class View:

    def show_message(self, message):
        print(message)

    def get_input(self, input_message):
        try:
            inp = input(input_message)
        except Exception as e:
            print(f"Error uccored: {e}")
            inp = None
        return inp

    def display_users(self, users):
        if users:
            print("\nList of Users:")
            for user in users:
                print(f"ID: {user.user_id}, Name: {user.name}")
        else:
            print("No users to display")

    def display_restaurants(self, restaurants):
        """Виведення списку ресторанів"""
        if restaurants:
            print("\nList of restaraunts:")
            for restaurant in restaurants:
                print(f"ID: {restaurant.restaurant_id}, Name: {restaurant.name}, Table Quantity: {restaurant.table_quantity}")
        else:
            print("No restaurants to display.")

    def show_restaurant_tables(self, restaurant_tables):
        """Виведення списку таблиць ресторану"""
        if restaurant_tables:
            print("\nList of restaraunt tables:")
            for table in restaurant_tables:
                print(f"Table ID: {table.table_id}, Capacity: {table.capacity}, Restaurant ID: {table.restaurant_id}")
        else:
            print("No restaurant tables to display.")

    def show_reservations(self, reservations):
        """Виведення списку бронювань"""
        if reservations:
            for reservation in reservations:
                print(f"Reservation ID: {reservation.reservation_id}, User ID: {reservation.user_id}, Table ID: {reservation.table_id}, Date: {reservation.reservation_date}, Duration: {reservation.duration} minutes")
        else:
            print("No reservations to display.")

    def show_contacts(self, contacts):
        """Виведення списку контактів"""
        if contacts:
            for contact in contacts:
                print(f"Contact ID: {contact.contact_id}, User ID: {contact.user_id}, Email: {contact.email}, Phone: {contact.phone}")
        else:
            print("No contacts to display.")

