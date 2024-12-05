import os
from datetime import datetime

# Data Storage
room_inventory = {}  # Stores room details
room_bookings = {}  # Stores room allocation details
DATA_FILE = "LHMS_Studentid.txt"

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    open(DATA_FILE, "w").close()


# Core Hotel Management Functions
def display_main_menu():
    print("\n=== LANGHAM Hotel Management System ===")
    print("1. Register New Room")
    print("2. Remove Room")
    print("3. Show All Room Details")
    print("4. Book a Room")
    print("5. View Room Booking Status")
    print("6. Generate Invoice & Release Room")
    print("7. Save Booking Data to File")
    print("8. Read Bookings from File")
    print("9. Backup Booking File and Clear Data")
    print("0. Exit")


def register_room():
    """Registers a new room in the system."""
    room_id = input("Enter the room ID: ")
    if room_id in room_inventory:
        print(f"Room {room_id} is already registered.")
        return

    try:
        category = input("Enter room category (e.g., Standard, Suite): ").strip()
        rate = float(input("Enter room rate (per night): ").strip())
        amenities = input("List amenities (separated by commas): ").strip().split(",")
        room_inventory[room_id] = {
            "category": category,
            "rate": rate,
            "amenities": [amenity.strip() for amenity in amenities]
        }
        print(f"Room {room_id} successfully registered.")
    except ValueError:
        print("Invalid input. Room registration failed.")


def delete_room():
    """Deletes a room from the system."""
    room_id = input("Enter the room ID to delete: ")
    if room_id in room_bookings:
        print(f"Room {room_id} is currently booked and cannot be deleted.")
    elif room_id in room_inventory:
        del room_inventory[room_id]
        print(f"Room {room_id} has been deleted.")
    else:
        print(f"Room {room_id} does not exist.")


def show_room_details():
    """Displays details of all registered rooms."""
    if not room_inventory:
        print("No rooms have been registered.")
        return

    print("\nRegistered Rooms:")
    for room_id, details in room_inventory.items():
        amenities = ", ".join(details["amenities"])
        print(f"Room ID: {room_id}, Category: {details['category']}, Rate: ${details['rate']}, Amenities: {amenities}")


def book_room():
    """Books a room for a customer."""
    room_id = input("Enter the room ID to book: ")
    if room_id not in room_inventory:
        print(f"Room {room_id} does not exist.")
        return

    if room_id in room_bookings:
        print(f"Room {room_id} is already booked by {room_bookings[room_id]}.")
    else:
        guest_name = input("Enter the guest's name: ").strip()
        room_bookings[room_id] = guest_name
        print(f"Room {room_id} successfully booked for {guest_name}.")


def view_bookings():
    """Displays the status of all booked rooms."""
    if not room_bookings:
        print("No rooms are currently booked.")
        return

    print("\nCurrent Bookings:")
    for room_id, guest_name in room_bookings.items():
        print(f"Room ID: {room_id}, Booked by: {guest_name}")


def generate_invoice_and_release():
    """Generates the bill for a booking and releases the room."""
    room_id = input("Enter the room ID to release: ")
    if room_id not in room_bookings:
        print(f"Room {room_id} is not currently booked.")
        return

    guest_name = room_bookings.pop(room_id)
    room_rate = room_inventory[room_id]["rate"]
    print(f"Invoice for {guest_name}:")
    print(f"Room ID: {room_id}, Total Amount: ${room_rate}")
    print(f"Room {room_id} is now available for booking.")


# File Handling Functions
def save_bookings_to_file():
    """Saves the current bookings to a file."""
    if not room_bookings:
        print("No bookings to save.")
        return

    try:
        with open(DATA_FILE, "w") as file:
            for room_id, guest_name in room_bookings.items():
                file.write(f"{room_id},{guest_name}\n")
        print(f"Booking data saved to {DATA_FILE}.")
    except IOError as e:
        print(f"Error saving data: {e}")


def read_bookings_from_file():
    """Reads bookings from the file and displays them."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        print(f"No data found in {DATA_FILE}.")
        return

    try:
        with open(DATA_FILE, "r") as file:
            print("\nBookings from File:")
            for line in file:
                room_id, guest_name = line.strip().split(",")
                print(f"Room ID: {room_id}, Booked by: {guest_name}")
    except IOError as e:
        print(f"Error reading file: {e}")


def backup_and_clear_file():
    """Backs up the booking file and clears its content."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        print(f"No data to backup in {DATA_FILE}.")
        return

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"Backup_LHMS_{timestamp}.txt"

        with open(DATA_FILE, "r") as original_file, open(backup_file, "w") as backup:
            backup.write(original_file.read())

        open(DATA_FILE, "w").close()  # Clear the original file
        print(f"Data backed up to {backup_file}. Original file cleared.")
    except IOError as e:
        print(f"Error during backup: {e}")


# Main Function
def main():
    while True:
        display_main_menu()
        try:
            option = input("Select an option: ").strip()
            if option == "1":
                register_room()
            elif option == "2":
                delete_room()
            elif option == "3":
                show_room_details()
            elif option == "4":
                book_room()
            elif option == "5":
                view_bookings()
            elif option == "6":
                generate_invoice_and_release()
            elif option == "7":
                save_bookings_to_file()
            elif option == "8":
                read_bookings_from_file()
            elif option == "9":
                backup_and_clear_file()
            elif option == "0":
                print("Thank you for using LANGHAM Hotel Management System. Goodbye!")
                break
            else:
                print("Invalid selection. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
