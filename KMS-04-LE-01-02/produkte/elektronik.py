#  Base class
from produkte.produkt import Produkt

#  Validator
from utils.validator import Validator


class Elektronik(Produkt):
    def __init__(self, name, price, weight, brand, warranty_years):
        super().__init__(name, price, weight)
        self.brand = brand
        self.warranty_years = warranty_years

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        if not Validator.validate_brand(value):
            raise ValueError("Invalid trademark.")
        self._brand = value

    @property
    def warranty_years(self):
        return self._warranty_years

    @warranty_years.setter
    def warranty_years(self, value):
        if not Validator.validate_warranty_years(value):
            raise ValueError("Invalid warranty period.")
        self._warranty_years = value

    def __str__(self):
        return (
            f"[Elektronik]\n"
            f"ID: {self.id} | Name: {self.name} | Preis: {self.price} € | Gewicht: {self.weight} kg\n"
            f"Marke: {self.brand} | Garantie: {self.warranty_years} Jahre"
        )
