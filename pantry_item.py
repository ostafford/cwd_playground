# 
from datetime import datetime
from typing import Dict, Optional
import uuid

class PantryItem:
    """
    Represents an item in the pantry with properties for tracking quantity and expiration.
    Demonstrates encapsulation, properties, and magic methods.
    """
    def __init__(
        self,
        name: str,
        category: str,
        quantity: float,
        unit: str,
        expiry_date: datetime
    ):
        # Private attributes are prefixed with underscore (_)
        # These can only be modified through properties with validation
        self._id = str(uuid.uuid4())
        # Constructor will auto-generate UUIDS.
        self._name = name
        self._category = category
        self._quantity = quantity
        self._unit = unit
        self._expiry_date = expiry_date

    # Property decorators for controlled access
    @property
    def id(self) -> str:
        """Getter for it'sm UUID."""
        return self._id

    @property
    def name(self) -> str:
        """Getter for item name"""
        return self._name

    @property
    def category(self) -> str:
        """Getter for item category"""
        return self._category

    @property
    def quantity(self) -> float:
        """
        'Getter' for quantity. Returns the current quantity of the item.
        """
        return self._quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        """
        Setter for quantity. Includes validation to prevent invalid values.
        Acts like a bank teller - checks if the operation is valid before proceeding.
        """
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value

    @property
    def unit(self) -> str:
        """Getter for item unit type"""
        return self._unit

    @property
    def expiry_date(self) -> datetime:
        """Getter for item expiry_date"""
        return self._expiry_date

    def is_expired(self) -> bool:
        """Check if the item is expired."""
        return datetime.now() > self._expiry_date

    def days_until_expiry(self) -> int:
        """Calculate days remaining until expiry."""
        # I might add a new column for days remaining for expiry
        delta = self._expiry_date - datetime.now()
        return max(0, delta.days)

    def __str__(self) -> str:
        """String representation for display to users."""
        base_info = f"{self._name} ({self._quantity} {self._unit}) - Category: {self._category}"

        if self.is_expired():
            return f"{base_info} - EXPIRED!"
        else:
            days = self.days_until_expiry()
            if days <= 7:
                return f"{base_info} - WARNING: Expires in {days} days"
            return f"{base_info} - Expires: {self._expiry_date.strftime('%d-%m-%Y')}"

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return (f"PantryItem(id='{self._id}', name='{self._name}', "
                f"category='{self._category}', quantity={self._quantity}, "
                f"unit='{self._unit}', expiry_date=datetime('{self._expiry_date.isoformat()}'))")

    def to_dict(self) -> Dict:
        """Convert item to dictionary for storage."""
        # Use this to save to JSON or CSV
        return {
            'id': self._id,
            'name': self._name,
            'category': self._category,
            'quantity': self._quantity,
            'unit': self._unit,
            'expiry_date': self._expiry_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PantryItem':
        """Create PantryItem instance from dictionary data."""
        return cls(
            name=data['name'],
            category=data['category'],
            quantity=data['quantity'],
            unit=data['unit'],
            expiry_date=datetime.fromisoformat(data['expiry_date'])
        )
