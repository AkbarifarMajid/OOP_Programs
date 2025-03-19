from produkte.produkt import Produkt
from storage.storage import Storage
from storage.exceptions import DatenbankFehler

class Kleidung(Produkt):
    def __init__(self, name, price, weight, size, color):
        super().__init__(name, price, weight)
        self.size = size
        self.color = color

    @staticmethod
    def get_all_clothing():
        try:
            result = Storage.fetch_all("SELECT * FROM produkte_kleidung")
            return result
        except DatenbankFehler as e:
            print("Fehler:", e)
            return None

    @staticmethod
    def get_clothing_by_id(id):
        try:
            result = Storage.fetch_one("SELECT * FROM produkte_kleidung WHERE id = %s", (id,))
            return result
        except DatenbankFehler as e:
            print("Fehler:", e)
            return None
