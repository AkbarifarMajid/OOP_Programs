#  Base class
from produkte.produkt import Produkt

#  Validator
from utils.validator import Validator


class Buch(Produkt):
    def __init__(self, name, price, weight, author, pages_count):
        super().__init__(name, price, weight)
        self.author = author
        self.pages_count = pages_count

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not Validator.validate_author(value):
            raise ValueError("❌ Ungültiger Autor.")
        self._author = value

    @property
    def pages_count(self):
        return self._pages_count

    @pages_count.setter
    def pages_count(self, value):
        if not Validator.validate_pages_count(value):
            raise ValueError("❌ Ungültige Seitenanzahl.")
        self._pages_count = value

    def __str__(self):
        return (
            f"[Buch]\n"
            f"ID: {self.id} | Titel: {self.name} | Preis: {self.price} € | Gewicht: {self.weight} kg\n"
            f"Autor: {self.author} | Seiten: {self.pages_count}"
        )
