from kunden.kunde import Kunde
from utils.validator import Validator
from storage.storage import Storage
from storage.exceptions import DatenbankFehler, SpeicherFehler

class Privatkunde(Kunde):
    def __init__(self, name, address, email, phone, password, birthdate):
        super().__init__(name, address, email, phone, password)
        if not Validator.validate_birthdate(birthdate):
            raise ValueError("Ungültiges Geburtsdatum.")
        self.birthdate = birthdate

    def __str__(self):
        return f"{self.name} | {self.email} | Privatkunde"

    @staticmethod
    def create_customer(name, address, email, phone, password, birthdate):
        try:
            #  Nur zur Validierung → wird nicht gespeichert
            _ = Privatkunde(name, address, email, phone, password, birthdate)

            # Insert into main table
            query1 = """
                INSERT INTO kunden (name, address, email, phone, password, kundentyp)
                VALUES (%s, %s, %s, %s, %s, 'privat')
            """
            kunde_id = Storage.insert_and_get_id(query1, (name, address, email, phone, password))

            # Insert into sub-table
            query2 = "INSERT INTO privatkunden (id, birthdate) VALUES (%s, %s)"
            Storage.execute_query(query2, (kunde_id, birthdate))

            return kunde_id
        except (ValueError, SpeicherFehler) as e:
            print("Fehler beim Erstellen des Privatkunden:", e)
            return None

    @staticmethod
    def get_all_privats():
        try:
            return Storage.fetch_all("SELECT * FROM privatkunden")
        except DatenbankFehler as e:
            print("Fehler beim Laden der Privatkunden:", e)
            return None

    @staticmethod
    def load_customer_by_id(kunde_id):
        try:
            # اطلاعات پایه از جدول 'kunden'
            row = Storage.fetch_one(
                "SELECT * FROM kunden WHERE id = %s AND kundentyp = 'privat'", (kunde_id,)
            )
            if not row:
                return None

            _, name, address, email, phone, password, _ = row

            # اطلاعات اضافی از جدول 'privatkunden'
            birth_row = Storage.fetch_one(
                "SELECT birthdate FROM privatkunden WHERE id = %s", (kunde_id,)
            )
            if not birth_row:
                return None

            kunde = Privatkunde(name, address, email, phone, password, str(birth_row[0]))
            kunde.id = kunde_id  # انتساب شناسه
            return kunde

        except DatenbankFehler as e:
            print("Fehler beim Laden des Privatkunden:", e)
            return None

    @staticmethod
    def get_privat_by_id(kunde_id):
        try:
            return Storage.fetch_one("SELECT * FROM privatkunden WHERE id = %s", (kunde_id,))
        except DatenbankFehler as e:
            print("Fehler:", e)
            return None

    def edit_customer(self):
        try:
            Storage.execute_query(
                "UPDATE kunden SET name=%s, address=%s, email=%s, phone=%s, password=%s WHERE id = %s",
                (self.name, self.address, self.email, self.phone, self.password, self.id)
            )

            Storage.execute_query(
                "UPDATE privatkunden SET birthdate = %s WHERE id = %s",
                (self.birthdate, self.id)
            )

        except SpeicherFehler as e:
            print("Fehler beim Aktualisieren des Privatkunden:", e)

