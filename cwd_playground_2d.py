"""Pantry management system with JSON and CSV storage capabilities."""

import json
import csv
from datetime import datetime

class Item:
    """Class representing an item in the pantry with its properties."""
    def __init__(self, name, quantity, unit, expiry_date):
        """Initialize an item with name, quantity, unit and expiry date."""
        self.name = name
        self.quantity = quantity
        self.unit = unit  # e.g., 'pieces', 'ml'
        self.expiry_date = expiry_date

    def __str__(self):
        """Return string representation of the item."""
        return f"{self.name} ({self.quantity}{self.unit}) expiring {self.expiry_date}"

    def to_dict(self):
        """Convert item to dictionary format."""
        return {
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
            "expiry_date": self.expiry_date.isoformat()
        }

class Pantry:
    """Class managing a collection of pantry items organized by categories."""
    def __init__(self):
        """Initialize pantry with empty categories and items lists."""
        self._categories = {}
        self._items = []
        # Load existing data - prioritize CSV, use JSON as backup
        try:
            self.load_from_csv("pantry.csv")
        except FileNotFoundError:
            try:
                self.load_from_json("pantry.json")
            except FileNotFoundError:
                pass

    def add_item(self):
        """Add a new item to the pantry with user input."""
        print("\nAdding a new item:")
        category_name = self._get_or_create_category()

        name = input("Enter item name: ")
        while True:
            try:
                quantity = int(input("Enter quantity: "))
                break
            except ValueError:
                print("Quantity must be an integer.")

        unit = input("Enter unit (e.g., ml, pieces): ").lower()

        # Handling date input
        while True:
            expiry_date_input = input("Enter expiry date (YYYY-MM-DD): ")
            try:
                expiry_date = datetime.strptime(expiry_date_input, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Try again.")

        new_item = Item(name=name, quantity=quantity, unit=unit, expiry_date=expiry_date)
        self._categories[category_name].append(new_item)

    def view_inventory(self):
        """Display all items in the pantry grouped by category."""
        # Check if any categories have items
        if not any(self._categories.values()):
            print("\nPantry is empty!")
            return

        print("\nInventory:")
        for category, items in self._categories.items():
            if not items or not category:  # Skip empty categories or None category names
                continue
            try:
                print(f"\n{category.capitalize()}")
                print("=" * 50)
                for item in items:
                    print(item)
            except AttributeError:
                print(f"\nCategory {category}")
                print("=" * 50)
                for item in items:
                    print(item)

    def delete_item(self):
        """Remove an item from the pantry based on user input."""
        # Check if pantry has any items
        if not any(self._categories.values()):
            print("\nPantry is empty!")
            return

        while True:
            try:
                item_name = input("Enter the name of the item to remove: ").lower()  # Convert to lowercase
                # Find the item and its category
                found = False
                for category, items in self._categories.items():
                    for item in items:
                        if item.name.lower() == item_name:  # Case-insensitive comparison
                            found = True
                            print(f"Found '{item.name}' with quantity {item.quantity}")
                            while True:
                                try:
                                    delete_qty = input("Enter quantity to remove (or 'all' to remove everything): ").lower()
                                    if delete_qty == 'all':
                                        items.remove(item)
                                        print(f"Removed all of '{item.name}' successfully.")
                                    else:
                                        qty = int(delete_qty)
                                        if qty <= 0:
                                            print("Please enter a positive number.")
                                            continue
                                        if qty >= item.quantity:
                                            items.remove(item)
                                            print(f"Removed all of '{item.name}' successfully.")
                                        else:
                                            item.quantity -= qty
                                            print(f"Removed {qty} of '{item.name}'. {item.quantity} remaining.")
                                    break
                                except ValueError:
                                    print("Please enter a valid number or 'all'.")
                            break
                    if found:
                        break
                
                if not found:
                    print(f"'{item_name}' not found.")
                return  # Exit after one successful operation
                
            except ValueError as e:
                print(f"Error: {e}")

    def load_from_json(self, filename):
        """Load pantry data from a JSON file."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for category_name in data:
                    category_items = []
                    for item_dict in data[category_name]:
                        expiry_date = datetime.fromisoformat(item_dict["expiry_date"])
                        item = Item(
                            name=item_dict["name"],
                            quantity=item_dict["quantity"],
                            unit=item_dict["unit"],
                            expiry_date=expiry_date
                        )
                        category_items.append(item)
                    self._categories[category_name] = category_items
        except FileNotFoundError:
            pass

    def save_to_json(self, filename):
        """Save pantry data to a JSON file."""
        data = {}
        for cat_name, items in self._categories.items():
            data[cat_name] = [item.to_dict() for item in items]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_from_csv(self, filename):
        """Load pantry data from a CSV file."""
        try:
            # First try UTF-8
            with open(filename, "r", encoding="utf-8", newline='') as f:
                reader = csv.DictReader(f)
                self._categories.clear()  # Clear existing data before loading
                for row in reader:
                    category = row['category']
                    if category not in self._categories:
                        self._categories[category] = []
                    
                    expiry_date = datetime.strptime(row['expiry_date'], "%Y-%m-%d").date()
                    item = Item(
                        name=row['name'],
                        quantity=int(row['quantity']),
                        unit=row['unit'],
                        expiry_date=expiry_date
                    )
                    self._categories[category].append(item)
        except UnicodeDecodeError:
            # If UTF-8 fails, try with a different encoding
            with open(filename, "r", encoding="latin-1", newline='') as f:
                reader = csv.DictReader(f)
                self._categories.clear()
                for row in reader:
                    category = row['category']
                    if category not in self._categories:
                        self._categories[category] = []
                    
                    expiry_date = datetime.strptime(row['expiry_date'], "%Y-%m-%d").date()
                    item = Item(
                        name=row['name'],
                        quantity=int(row['quantity']),
                        unit=row['unit'],
                        expiry_date=expiry_date
                    )
                    self._categories[category].append(item)

    def save_to_csv(self, filename):
        """Save pantry data to a CSV file."""
        fieldnames = ['category', 'name', 'quantity', 'unit', 'expiry_date']
        with open(filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for category, items in self._categories.items():
                for item in items:
                    writer.writerow({
                        'category': category,
                        'name': item.name,
                        'quantity': item.quantity,
                        'unit': item.unit,
                        'expiry_date': item.expiry_date.strftime("%Y-%m-%d")
                    })

    def _get_or_create_category(self):
        """Get existing category or create a new one based on user input."""
        print("\nCategories available:")
        for idx, cat in enumerate(self._categories.keys(), 1):
            print(f"{idx}. {cat}")
        print(f"\n{len(self._categories)+1}. Create new category")

        while True:
            try:
                choice = int(input("Enter the number of the category or create a new one: "))
                if 0 < choice <= len(self._categories):
                    return list(self._categories.keys())[choice-1]
                if choice == len(self._categories)+1:
                    new_cat = input("Enter new category name: ")
                    if new_cat in self._categories:
                        print("Category already exists!")
                        continue
                    self._categories[new_cat] = []
                    return new_cat
                print("Invalid option. Please choose again.")
            except ValueError:
                print("Please enter a number.")

def main():
    """Main function to run the pantry management system."""
    pantry = Pantry()

    while True:
        print("\nOptions:")
        print("1. Add an item")
        print("2. View inventory")
        print("3. Delete an item")
        print("4. Exit")

        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if choice == 1:
                pantry.add_item()
            elif choice == 2:
                pantry.view_inventory()
            elif choice == 3:
                pantry.delete_item()
            elif choice == 4:
                print("Exiting program...")
                pantry.save_to_json("pantry.json")  # Keep JSON backup
                pantry.save_to_csv("pantry.csv")    # Primary storage method
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
