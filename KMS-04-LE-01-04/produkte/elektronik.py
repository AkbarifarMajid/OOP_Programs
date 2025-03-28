from produkte.produkt import Produkt
from storage.storage import Storage
from utils.validator import Validator
from storage.exceptions import DatenbankFehler

class Elektronik(Produkt):
    def __init__(self, name, price, weight, brand, warranty_years):
        super().__init__(name, price, weight)
        self.brand = brand
        self.warranty_years = warranty_years

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f" Name: {self.name}\n"
            f" Preis: {self.price} €\n"
            f" Gewicht: {self.weight} kg\n"
            f" Marke: {self.brand}\n"
            f" Garantie: {self.warranty_years} Jahre\n"
            f" Typ: Elektronik"
        )

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        if not Validator.validate_brand(value):
            raise ValueError("Invalid brand.")
        self._brand = value

    @property
    def warranty_years(self):
        return self._warranty_years

    @warranty_years.setter
    def warranty_years(self, value):
        if not Validator.validate_warranty_years(value):
            raise ValueError("Invalid warranty duration.")
        self._warranty_years = value

    @staticmethod
    def get_all_electronics():
        query = '''
            SELECT p.id, p.name, p.price, p.weight, e.brand, e.warranty_years
            FROM produkte p
            JOIN produkte_elektronik e ON p.id = e.id
            WHERE p.kategorie = 'elektronik'
        '''
        return Storage.fetch_all(query)

    @staticmethod
    def get_electronic_by_id(id):
        query = '''
            SELECT p.id, p.name, p.price, p.weight, e.brand, e.warranty_years
            FROM produkte p
            JOIN produkte_elektronik e ON p.id = e.id
            WHERE p.id = %s AND p.kategorie = 'elektronik'
        '''
        return Storage.fetch_one(query, (id,))
