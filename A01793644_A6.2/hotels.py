"""
This module contains functions for processing data using sys, and collections.
"""
import json
import os
import sys

class Persistent:
    """
    This module class functions for processing data using sys, and collections.
    """
    data_folder = "data_storage"

    def __init__(self, filename):
        self.filename = os.path.join(self.data_folder, filename)
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w', encoding='UTF-8') as file:
                json.dump([], file)

    def read_data(self):
        """
        This function for processing data
        """
        with open(self.filename, 'r',encoding='UTF-8') as file:
            return json.load(file)

    def write_data(self, data):
        """
        This function for processing data
        """
        with open(self.filename, 'w',encoding='UTF-8') as file:
            json.dump(data, file, indent=4)

def int_validation(value):
    """
    Validates if the value is an integer and optionally within a specified range.
    
    :param value: The value to validate.
    :param min_value: Optional minimum value constraint.
    :param max_value: Optional maximum value constraint.
    :return: True if value is valid, False otherwise.
    """
    if not isinstance(value, int):
        return False
    return True

def str_validation(value):
    """
    Validates if the value is a string and optionally checks the length constraints.
    
    :param value: The value to validate.
    :param min_length: Optional minimum length constraint.
    :param max_length: Optional maximum length constraint.
    :return: True if value is valid, False otherwise.
    """
    if not isinstance(value, str):
        return False
    return True


class Hotel(Persistent):
    """
    This module class functions for processing data hotels using sys, and collections.
    """
    def __init__(self):
        super().__init__("hotels.json")

    def create_hotel(self, hotel_id:int, name:str, location:str, rooms:int):
        """
        This function for processing data
        """
        if not int_validation(hotel_id):
            print("Error: hotel_id must be an integer.")
            return
        if not int_validation(rooms):
            print("Error: hotel_id must be an integer.")
            return
        if not str_validation(name):
            print("Error: name must be a string.")
            return
        if not str_validation(location):
            print("Error: name must be a string.")
            return
        hotels = self.read_data()
        if hotel_id not in [hotel['hotel_id'] for hotel in hotels]:
            hotels.append({"hotel_id": hotel_id, "name": name,\
                            "location": location, "rooms": rooms})
            self.write_data(hotels)
            print(f"Hotel '{name}' added successfully.")
        else:
            print(f"Hotel with ID '{hotel_id}' already exists.")

    def delete_hotel(self, hotel_id:int):
        """
        This function for processing data
        """
        if not int_validation(hotel_id):
            print("Error: hotel_id must be an integer.")
            return
        hotels = self.read_data()
        hotels = [hotel for hotel in hotels if hotel['hotel_id'] != hotel_id]
        self.write_data(hotels)
        print(f"Hotel with ID '{hotel_id}' has been deleted.")

    def display_hotel(self, hotel_id:int):
        """
        This function for processing data
        """
        if not int_validation(hotel_id):
            print("Error: hotel_id must be an integer.")
            return
        hotels = self.read_data()
        hotel = next((hotel for hotel in hotels if hotel['hotel_id'] == hotel_id), None)
        if hotel:
            print(f"Hotel ID: {hotel['hotel_id']}\nName: {hotel['name']}\nLocation:\
                   {hotel['location']}\nRooms: {hotel['rooms']}")
        else:
            print(f"Hotel with ID '{hotel_id}' not found.")

    def modify_hotel(self, hotel_id:int, name=None, location=None, rooms=None):
        """
        This function for processing data
        """
        if not int_validation(hotel_id):
            print("Error: hotel_id must be an integer.")
            return
        hotels = self.read_data()
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                if name:
                    hotel['name'] = name
                if location:
                    hotel['location'] = location
                if rooms:
                    hotel['rooms'] = rooms
                self.write_data(hotels)
                print(f"Hotel '{hotel_id}' updated successfully.")
                return
        print(f"Hotel with ID '{hotel_id}' not found.")

    def reserve_room(self, reservation_id:int, hotel_id:int, customer_id:int, room_number:int):
        """
        This function for processing data
        """
        if not int_validation(hotel_id):
            print("Error: hotel_id must be an integer.")
            return
        if not int_validation(reservation_id):
            print("Error: hotel_id must be an integer.")
            return
        if not int_validation(customer_id):
            print("Error: hotel_id must be an integer.")
            return
        if not str_validation(room_number):
            print("Error: hotel_id must be an integer.")
            return
        reservations = Reservation().read_data()
        if any(reservation['room_number'] == room_number \
               for reservation in reservations if reservation['hotel_id'] == hotel_id):
            print(f"Room {room_number} in Hotel ID '{hotel_id}' is already reserved.")
        else:
            reservations.append({"reservation_id": reservation_id, \
                                 "hotel_id": hotel_id, "customer_id": customer_id,\
                                      "room_number": room_number})
            Reservation().write_data(reservations)
            print(f"Room {room_number} in Hotel ID '{hotel_id}' reserved successfully.")

    def cancel_reservation(self, reservation_id:int):
        """
        This function for processing data
        """
        if not int_validation(reservation_id):
            print("Error: hotel_id must be an integer.")
            return
        reservations = Reservation().read_data()
        reservations = [reservation for reservation in reservations \
                        if reservation['reservation_id'] != reservation_id]
        Reservation().write_data(reservations)
        print(f"Reservation ID '{reservation_id}' has been cancelled.")


class Customer(Persistent):
    """
    This module class functions for processing data customer using sys, and collections.
    """
    def __init__(self):
        super().__init__("customers.json")

    def create_customer(self, customer_id:int, name:str, email:str):
        """
        This function for processing data
        """
        if not int_validation(customer_id):
            print("Error: hotel_id must be an integer.")
            return
        if not str_validation(name):
            print("Error: hotel_id must be an integer.")
            return
        if not str_validation(email):
            print("Error: hotel_id must be an integer.")
            return
        customers = self.read_data()
        if customer_id not in [customer['customer_id'] for customer in customers]:
            customers.append({"customer_id": customer_id, "name": name, "email": email})
            self.write_data(customers)
            print(f"Customer '{name}' added successfully.")
        else:
            print(f"Customer with ID '{customer_id}' already exists.")

    def delete_customer(self, customer_id:int):
        """
        This function for processing data
        """
        if not int_validation(customer_id):
            print("Error: hotel_id must be an integer.")
            return
        customers = self.read_data()
        customers = [customer for customer in customers if customer['customer_id'] != customer_id]
        self.write_data(customers)
        print(f"Customer with ID '{customer_id}' has been deleted.")

    def display_customer(self, customer_id:int):
        """
        This function for processing data
        """
        if not int_validation(customer_id):
            print("Error: hotel_id must be an integer.")
            return
        customers = self.read_data()
        customer = next((customer for customer in customers \
                         if customer['customer_id'] == customer_id), None)
        if customer:
            print(f"Customer ID: {customer['customer_id']}\nName: \
                  {customer['name']}\nEmail: {customer['email']}")
        else:
            print(f"Customer with ID '{customer_id}' not found.")

    def modify_customer(self, customer_id:int, name=None, email=None):
        """
        This function for processing data
        """
        if not int_validation(customer_id):
            print("Error: hotel_id must be an integer.")
            return
        customers = self.read_data()
        for customer in customers:
            if customer['customer_id'] == customer_id:
                if name:
                    customer['name'] = name
                if email:
                    customer['email'] = email
                self.write_data(customers)
                print(f"Customer '{customer_id}' updated successfully.")
                return
        print(f"Customer with ID '{customer_id}' not found.")


class Reservation(Persistent):
    """
    This module class functions for processing data reservation using sys, and collections.
    """
    def __init__(self):
        super().__init__("reservations.json")

    def create_reservation(self, reservation_id:int, customer_id:int, hotel_id:int,
                           room_number:int, start_date:str, end_date:str):
        """
        This function for processing data
        """
        if not int_validation(customer_id):
            print("Error: hotel_id must be an integer.")
            return
        if not int_validation(reservation_id):
            print("Error: hotel_id must be an integer.")
            return
        if not int_validation(hotel_id):
            print("Error: hotel_id must be an integer.")
            return
        if not int_validation(room_number):
            print("Error: hotel_id must be an integer.")
            return
        reservations = self.read_data()
        # Check if the reservation ID already exists to avoid duplicates
        if reservation_id in [reservation['reservation_id'] for reservation in reservations]:
            print(f"Reservation with ID '{reservation_id}' already exists.")
            return

        # Check if the room is already reserved
        for reservation in reservations:
            if reservation['hotel_id'] == hotel_id and reservation['room_number'] == room_number:
                print(f"Room {room_number} in Hotel ID '{hotel_id}' is already reserved.")
                return

        # Assuming validation for customer_id and hotel_id existence is done elsewhere
        reservations.append({
            "reservation_id": reservation_id,
            "customer_id": customer_id,
            "hotel_id": hotel_id,
            "room_number": room_number,
            "start_date": start_date,
            "end_date": end_date
        })
        self.write_data(reservations)
        print(f"Reservation '{reservation_id}' for Customer ID '{customer_id}'\
               in Hotel ID '{hotel_id}' created successfully.")

    def cancel_reservation(self, reservation_id):
        """
        This function for processing data
        """
        if not int_validation(reservation_id):
            print("Error: hotel_id must be an integer.")
            return
        reservations = self.read_data()
        # Filter out the reservation to be canceled
        new_reservations = [reservation for reservation in reservations \
                             if reservation['reservation_id'] != reservation_id]
        if len(reservations) == len(new_reservations):
            print(f"No reservation found with ID '{reservation_id}'.")
        else:
            self.write_data(new_reservations)
            print(f"Reservation ID '{reservation_id}' has been cancelled.")


def hotel_cli(hotel_manager):
    """
    This module class functions as a cli manager for hotels
    """
    reservation_manager = Reservation()
    while True:
        print("\nHotel Management:")
        print("1. Create Hotel")
        print("2. Delete Hotel")
        print("3. Display Hotel Information")
        print("4. Modify Hotel Information")
        print("5. Reserve a Room")
        print("6. Cancel a Reservation")
        print("7. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            hotel_id = input("Enter Hotel ID: ")
            name = input("Enter Hotel Name: ")
            location = input("Enter Hotel Location: ")
            rooms = int(input("Enter Number of Rooms: "))  # Simple input, no validation added here
            hotel_manager.create_hotel(hotel_id, name, location, rooms)
        elif choice == "2":
            hotel_id = input("Enter Hotel ID to delete: ")
            hotel_manager.delete_hotel(hotel_id)
        elif choice == "3":
            hotel_id = input("Enter Hotel ID to display: ")
            hotel_manager.display_hotel(hotel_id)
        elif choice == "4":
            hotel_id = input("Enter Hotel ID to modify: ")
            name = input("Enter new name (leave blank to keep current): ")
            location = input("Enter new location (leave blank to keep current): ")
            rooms = input("Enter new number of rooms (leave blank to keep current): ")
            rooms = int(rooms) if rooms else None
            hotel_manager.modify_hotel(hotel_id, name, location, rooms)
        elif choice == "5":
            # Assuming reserve_room is defined in the Reservation class
            reservation_id = input("Enter Reservation ID: ")
            hotel_id = input("Enter Hotel ID: ")
            customer_id = input("Enter Customer ID: ")
            room_number = input("Enter Room Number: ")
            reservation_manager.create_reservation(reservation_id, customer_id, \
                                                   hotel_id, room_number, "start_date", "end_date")
        elif choice == "6":
            # Assuming cancel_reservation is defined in the Reservation class
            reservation_id = input("Enter Reservation ID to cancel: ")
            reservation_manager.cancel_reservation(reservation_id)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

def customer_cli(customer_manager):
    """
    This module class functions as a cli manager for customers
    """
    while True:
        print("\nCustomer Management:")
        print("1. Create Customer")
        print("2. Delete Customer")
        print("3. Display Customer Information")
        print("4. Modify Customer Information")
        print("5. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            customer_id = input("Enter Customer ID: ")
            name = input("Enter Customer Name: ")
            email = input("Enter Customer Email: ")
            customer_manager.create_customer(customer_id, name, email)
        elif choice == "2":
            customer_id = input("Enter Customer ID to delete: ")
            customer_manager.delete_customer(customer_id)
        elif choice == "3":
            customer_id = input("Enter Customer ID to display: ")
            customer_manager.display_customer(customer_id)
        elif choice == "4":
            customer_id = input("Enter Customer ID to modify: ")
            name = input("Enter new name (leave blank to keep current): ")
            email = input("Enter new email (leave blank to keep current): ")
            customer_manager.modify_customer(customer_id, name if name \
                                             else None, email if email else None)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def reservation_cli(reservation_manager):
    """
    This module class functions as a cli manager for reservations
    """
    while True:
        print("\nReservation Management:")
        print("1. Create Reservation")
        print("2. Cancel Reservation")
        print("3. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            reservation_id = input("Enter Reservation ID: ")
            customer_id = input("Enter Customer ID: ")
            hotel_id = input("Enter Hotel ID: ")
            room_number = input("Enter Room Number: ")
            start_date = input("Enter Start Date (YYYY-MM-DD): ")
            end_date = input("Enter End Date (YYYY-MM-DD): ")
            reservation_manager.create_reservation(reservation_id, customer_id,\
                                                    hotel_id, room_number, start_date, end_date)
        elif choice == "2":
            reservation_id = input("Enter Reservation ID to cancel: ")
            reservation_manager.cancel_reservation(reservation_id)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    """
    This module class functions as a cli manager for main program
    """
    hotel_manager = Hotel()
    customer_manager = Customer()
    reservation_manager = Reservation()

    while True:
        print("\nMenu:")
        print("1. Hotel")
        print("2. Customer")
        print("3. Reservation")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            hotel_cli(hotel_manager)
        elif choice == "2":
            customer_cli(customer_manager)

        elif choice == "3":
            reservation_cli(reservation_manager)

        elif choice == "4":
            print("Exiting the program.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
