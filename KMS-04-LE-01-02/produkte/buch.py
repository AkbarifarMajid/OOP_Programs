from produkte.produkt import Produkt
from storage.storage import Storage
from storage.exceptions import DatenbankFehler, NichtGefundenFehler


class Buch(Produkt):
    def __init__(self, name, price, weight, author, pages_count):
        super().__init__(name, price, weight)
        self.author = author
        self.pages_count = pages_count

    @staticmethod
    def get_all_books():
        try:
            result = Storage.fetch_all("SELECT * FROM produkte_buch")
            return result
        except DatenbankFehler as e:
            print("Fehler:", e)
            return None

    @staticmethod
    def get_book_by_id(id):
        try:
            result = Storage.fetch_one("SELECT * FROM produkte_buch WHERE id = %s", (id,))
            return result
        except DatenbankFehler as e:
            print("Fehler:", e)
            return None

