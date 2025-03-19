from kunden.kunde import Kunde
from utils.validator import Validator
from storage.storage import Storage
from storage.exceptions import DatenbankFehler, SpeicherFehler

class Privatkunde(Kunde):
    def __init__(self, name, address, email, phone, password, birthdate):
        super().__init__(name, address, email, phone, password)
        if not Validator.validate_birthdate(birthdate):
            raise ValueError(" Geburtsdatum ist nicht gültig.")
        self.birthdate = birthdate

    def __str__(self):
        # Returns a detailed string with all relevant private customer information
        return (
            f"Name: {self.name}\n"
            f" E-Mail: {self.email}\n"
            f" Adresse: {self.address}\n"
            f" Telefon: {self.phone}\n"
            f" Passwort: {self.password}\n"
            f" Geburtsdatum: {self.birthdate}\n"
            f" Typ: Privatkunde"
        )

    # Creates and saves a new Privat Costumer in the database.
    @staticmethod
    def create_customer(name, address, email, phone, password, birthdate):
            #  Nur zur Validierung
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

    # Loads all entries from the 'Privat Costumer' table.
    @staticmethod
    def get_all_privats():
        return Storage.fetch_all("SELECT * FROM privatkunden")

    #Retrieves a single Private kunde from the database by ID.
    @staticmethod
    def get_privat_by_id(kunde_id):
        return Storage.fetch_one("SELECT * FROM privatkunden WHERE id = %s", (kunde_id,))

    @staticmethod
    def delete_customer(db_kunde_id):
        Storage.execute_query("DELETE FROM kunden WHERE id = %s", (db_kunde_id,))

    # Updates the information of an existing Private kunde  in the database.
    def edit_customer(self):
        Storage.execute_query(
            "UPDATE kunden SET name=%s, address=%s, email=%s, phone=%s, password=%s WHERE id = %s",
            (self.name, self.address, self.email, self.phone, self.password, self.id)
        )

        Storage.execute_query(
             "UPDATE privatkunden SET birthdate = %s WHERE id = %s",
            (self.birthdate, self.id)
        )


    '''
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
    def edit_customer(kunde_id, name, address, email, phone, password, birthdate):
        try:
            # Update in main table
            query1 = """
                UPDATE kunden
                SET name = %s, address = %s, email = %s, phone = %s, password = %s
                WHERE id = %s
            """
            Storage.execute_query(query1, (name, address, email, phone, password, kunde_id))
    
            # Update in sub-table
            query2 = "UPDATE privatkunden SET birthdate = %s WHERE id = %s"
            Storage.execute_query(query2, (birthdate, kunde_id))
    
            print(f"Privatkunde mit ID {kunde_id} wurde aktualisiert.")
        except SpeicherFehler as e:
            print("Fehler beim Aktualisieren des Privatkunden:", e)
         

    '''