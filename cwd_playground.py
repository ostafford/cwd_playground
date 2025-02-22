"""Simple pantry inventory management system."""

# Inventory list (can hold dictionaries for items)
inventory = []


# Function to display the menu
def display_menu():
    """Display the main menu options for the pantry inventory system."""
    print("=== Pantry Inventory Menu ===")
    print("1. Add Item")
    print("2. Remove Item")
    print("3. Display Inventory")
    print("4. Calculate Total Value")
    print("5. Exit")


# Function to add an item
def add_item():
<<<<<<< HEAD
    pass # just adding comment to confirm new branch creation
=======
    """Add a new item to the pantry inventory."""
    name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price per unit: "))
    inventory.append({"name": name, "quantity": quantity, "price": price})
>>>>>>> UML_Design


# Function to remove an item
def remove_item():
    """Remove an item from the pantry inventory."""
    pass


# Function to display the inventory
def display_inventory():
    """Display all items currently in the pantry inventory."""
    print("===Inventory:===")
    if not inventory:
        print("Inventory is empty.")
        return
    for item in inventory:
        print(f"{item['name']}: {item['quantity']} units at ${item['price']} each")


# Function to calculate total value
def calculate_total_value():
    """Calculate and display the total value of all inventory items."""
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
