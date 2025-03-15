#  Base class
from produkte.produkt import Produkt

#  Validator
from utils.validator import Validator

class Kleidung(Produkt):
    def __init__(self, name, price, weight, size, color):
        super().__init__(name, price, weight)
        self.size = size
        self.color = color

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if not Validator.validate_size(value):
            raise ValueError("❌ Ungültige Größe.")
        self._size = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not Validator.validate_color(value):
            raise ValueError("❌ Ungültige Farbe.")
        self._color = value

    def __str__(self):
        return (
            f"[Kleidung]\n"
            f"ID: {self.id} | Name: {self.name} | Preis: {self.price} € | Gewicht: {self.weight} kg\n"
            f"Größe: {self.size} | Farbe: {self.color}"
        )
