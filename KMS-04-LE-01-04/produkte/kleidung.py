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

    @staticmethod
    def get_all_clothing():
        query = '''
            SELECT p.id, p.name, p.price, p.weight, k.size, k.color
            FROM produkte p
            JOIN produkte_kleidung k ON p.id = k.id
            WHERE p.kategorie = 'kleidung'
        '''
        return Storage.fetch_all(query)

    @staticmethod
    def get_clothing_by_id(id):
        query = '''
            SELECT p.id, p.name, p.price, p.weight, k.size, k.color
            FROM produkte p
            JOIN produkte_kleidung k ON p.id = k.id
            WHERE p.id = %s AND p.kategorie = 'kleidung'
        '''
        return Storage.fetch_one(query, (id,))
