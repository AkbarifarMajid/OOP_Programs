from produkte.produkt import Produkt
from storage.storage import Storage
from storage.exceptions import DatenbankFehler

class Elektronik(Produkt):
    def __init__(self, name, price, weight, brand, warranty_years):
        super().__init__(name, price, weight)
        self.brand = brand
        self.warranty_years = warranty_years

    @staticmethod
    def get_all_electronics():
        try:
            result = Storage.fetch_all("SELECT * FROM produkte_elektronik")
            return result
        except DatenbankFehler as e:
            print("Fehler:", e)
            return None

    @staticmethod
    def get_electronic_by_id(id):
        try:
            result = Storage.fetch_one("SELECT * FROM produkte_elektronik WHERE id = %s", (id,))
            return result
        except DatenbankFehler as e:
            print("Fehler:", e)
            return None
