# Inventory list (can hold dictionaries for items)
inventory = []


# Function to display the menu
def display_menu():
    print("=== Pantry Inventory Menu ===")
    print("1. Add Item")
    print("2. Remove Item")
    print("3. Display Inventory")
    print("4. Calculate Total Value")
    print("5. Exit")


# Function to add an item
def add_item():
    pass # just adding comment to confirm new branch creation


# Function to remove an item
def remove_item():
    pass


# Function to display the inventory
def display_inventory():
    pass


# Function to calculate total value
def calculate_total_value():
    pass


# Main program loop
while True:
    display_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        add_item()
    elif choice == "2":
        remove_item()
    elif choice == "3":
        display_inventory()
    elif choice == "4":
        calculate_total_value()
    elif choice == "5":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
