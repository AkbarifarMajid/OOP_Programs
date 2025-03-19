from abc import ABC, abstractmethod
from utils.validator import Validator

class Produkt(ABC):
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight

    @property
    def id(self):
        return self._id if hasattr(self, "_id") else None

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not Validator.validate_product_name(value):
            raise ValueError("Invalid product name.")
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not Validator.validate_price(value):
            raise ValueError("Invalid product Preis.")
        self._price = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not Validator.validate_weight(value):
            raise ValueError("Invalid weight.")
        self._weight = value
    @abstractmethod
    def __str__(self):
        pass
