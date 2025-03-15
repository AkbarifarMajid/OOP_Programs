#  Base for all products
from abc import ABC, abstractmethod
from utils.validator import Validator

class Produkt(ABC):
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight
        self.reviews = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not Validator.validate_product_name(value):
            raise ValueError("❌ Ungültiger Produktname.")
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not Validator.validate_price(value):
            raise ValueError("❌ Ungültiger Preis.")
        self._price = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not Validator.validate_weight(value):
            raise ValueError("❌ Ungültiges Gewicht.")
        self._weight = value

    @property
    def id(self):
        return self._id if hasattr(self, "_id") else None

    def add_review(self, rating):
        if 1 <= rating <= 5:
            self.reviews.append(rating)
        else:
            raise ValueError("❌ Bewertung muss zwischen 1 und 5 liegen.")

    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(self.reviews) / len(self.reviews)

    @abstractmethod
    def __str__(self):
        pass  # subclasses (Buch, Elektronik...) must implement this
