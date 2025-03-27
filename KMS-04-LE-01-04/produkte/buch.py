from produkte.produkt import Produkt
from storage.storage import Storage
from utils.validator import Validator
from storage.exceptions import DatenbankFehler, NichtGefundenFehler

class Buch(Produkt):
    def __init__(self, name, price, weight, author, pages_count):
        super().__init__(name, price, weight)
        self.author = author
        self.pages_count = pages_count

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f" Name: {self.name}\n"
            f" Preis: {self.price} €\n"
            f" Gewicht: {self.weight} kg\n"
            f" Autor: {self.author}\n"
            f" Seitenanzahl: {self.pages_count}\n"
            f" Typ: Buch"
        )

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not Validator.validate_author(value):
            raise ValueError("Invalid author.")
        self._author = value

    @property
    def pages_count(self):
        return self._pages_count

    @pages_count.setter
    def pages_count(self, value):
        if not Validator.validate_pages_count(value):
            raise ValueError("Invalid page count.")
        self._pages_count = value

    @staticmethod
    def get_all_books():
        query = '''
            SELECT p.id, p.name, p.price, p.weight, b.author, b.pages_count
            FROM produkte p
            JOIN produkte_buch b ON p.id = b.id
            WHERE p.kategorie = 'buch'
        '''
        return Storage.fetch_all(query)

    @staticmethod
    def get_book_by_id(id):
        query = '''
            SELECT p.id, p.name, p.price, p.weight, b.author, b.pages_count
            FROM produkte p
            JOIN produkte_buch b ON p.id = b.id
            WHERE p.id = %s AND p.kategorie = 'buch'
        '''
        return Storage.fetch_one(query, (id,))
'''
    @staticmethod
    def load_by_id(id):
        row = Buch.get_book_by_id(id)
        if not row:
            return None
        buch = Buch(
            name=row[1],
            price=row[2],
            weight=row[3],
            author=row[4],
            pages_count=row[5]
        )
        buch.id = row[0]
        return buch

'''