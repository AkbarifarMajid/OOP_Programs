from produkte.produkt import Produkt
from storage.storage import Storage
from utils.validator import Validator
from storage.exceptions import DatenbankFehler

class Kleidung(Produkt):
    def __init__(self, name, price, weight, size, color):
        super().__init__(name, price, weight)
        self.size = size
        self.color = color

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f" Name: {self.name}\n"
            f" Preis: {self.price} €\n"
            f" Gewicht: {self.weight} kg\n"
            f" Größe: {self.size}\n"
            f" Farbe: {self.color}\n"
            f" Typ: Kleidung"
        )

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if not Validator.validate_size(value):
            raise ValueError("Invalid size.")
        self._size = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not Validator.validate_color(value):
            raise ValueError("Invalid color.")
        self._color = value

    # Load alle Clothes from Datenbank
    @staticmethod
    def get_all_clothing():
        return  Storage.fetch_all("SELECT * FROM produkte_kleidung")

    # Load one Clothes from Datenbank bei ID
    #@staticmethod
    #def get_clothing_by_id(id):
       # return Storage.fetch_one("SELECT * FROM produkte_kleidung WHERE id = %s", (id,))

    @staticmethod
    def get_clothing_by_id(id):
        row = Storage.fetch_one("SELECT * FROM produkte_kleidung WHERE id = %s", (id,))
        if not row:
            return None

        produkt_id, size, color = row

        base = Storage.fetch_one(
            "SELECT name, price, weight FROM produkte WHERE id = %s AND kategorie = 'kleidung'", (id,)
        )
        if not base:
            return None

        name, price, weight = base
        k = Kleidung(name, price, weight, size, color)
        k.id = id
        return k
