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

    # Load alle Buch from Datenbank
    @staticmethod
    def get_all_books():
        return Storage.fetch_all("SELECT * FROM produkte_buch")

    #Load one Buch from Datenbank bei ID
    #@staticmethod
    #def get_book_by_id(id):
        #return  Storage.fetch_one("SELECT * FROM produkte_buch WHERE id = %s", (id,))

    @staticmethod
    def get_book_by_id(id):
        row = Storage.fetch_one("SELECT * FROM produkte_buch WHERE id = %s", (id,))
        if not row:
            return None

        produkt_id, author, pages_count = row

        base = Storage.fetch_one(
            "SELECT name, price, weight FROM produkte WHERE id = %s AND kategorie = 'buch'", (id,)
        )
        if not base:
            return None

        name, price, weight = base
        b = Buch(name, price, weight, author, pages_count)
        b.id = id
        return b
