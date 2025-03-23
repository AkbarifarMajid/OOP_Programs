from kunden.kunde import Kunde
from utils.validator import Validator
from storage.storage import Storage
from storage.exceptions import DatenbankFehler, SpeicherFehler

class Firmenkunde(Kunde):
    def __init__(self, name, address, email, phone, password, company_number):
        super().__init__(name, address, email, phone, password)
        if not Validator.validate_company_number(company_number):
            raise ValueError(" Firmennummer ist nicht gültig.")
        self.company_number = company_number

    def __str__(self):
        # Returns a detailed string with all relevant company customer information
        return (
            f" Firmenname: {self.name}\n"
            f" E-Mail: {self.email}\n"
            f" Adresse: {self.address}\n"
            f" Telefon: {self.phone}\n"
            f" Passwort: {self.password}\n"
            f"🏷 Firmennummer: {self.company_number}\n"
            f" Typ: Firmenkunde"
        )

    #Creates and saves a new Firmenkunde in the database.
    @staticmethod
    def create_customer(name, address, email, phone, password, company_number):
        # Vorab prüfen, ob E-Mail schon existiert
        existing = Storage.fetch_one("SELECT id FROM kunden WHERE email = %s", (email,))
        if existing:
            print("Ein Kunde mit dieser E-Mail existiert bereits.")
            return None

        #  Validierung der Eingabedaten
        _ = Firmenkunde(name, address, email, phone, password, company_number)

        #  In Haupttabelle einfügen
        query1 = """
            INSERT INTO kunden (name, address, email, phone, password, kundentyp)
            VALUES (%s, %s, %s, %s, %s, 'firma')
        """
        kunde_id = Storage.insert_and_get_id(query1, (name, address, email, phone, password))

        # In Firmentabelle einfügen
        query2 = "INSERT INTO firmenkunden (id, company_number) VALUES (%s, %s)"
        Storage.execute_query(query2, (kunde_id, company_number))

        return kunde_id

    #Loads all entries from the 'firmenkunden' table
    @staticmethod
    def get_all_firmen_kunde():
        rows = Storage.fetch_all("SELECT id, company_number FROM firmenkunden")
        kunden = []

        for row in rows:
            kunde_id, company_number = row
            base = Storage.fetch_one(
                "SELECT name, address, email, phone, password FROM kunden WHERE id = %s AND kundentyp = 'firma'",
                (kunde_id,)
            )

            if base:
                name, address, email, phone, password = base
                kunde = Firmenkunde(name, address, email, phone, password, company_number)
                kunde.id = kunde_id
                kunden.append(kunde)

        return kunden

    #Retrieves a single Firmenkunde (company customer) from the database by ID.
    @staticmethod
    def get_firma_by_id(kunde_id):
        row = Storage.fetch_one("SELECT * FROM firmenkunden WHERE id = %s", (kunde_id,))
        if not row:
            return None

        company_number = row[1]

        base = Storage.fetch_one(
            "SELECT name, address, email, phone, password FROM kunden WHERE id = %s AND kundentyp = 'firma'",
            (kunde_id,))
        if not base:
            return None

        name, address, email, phone, password = base
        kunde = Firmenkunde(name, address, email, phone, password, company_number)
        kunde.id = kunde_id
        return kunde

    # Updates the information of an existing Firmenkunde in the database.
    def edit_customer(self):
        Storage.execute_query(
            "UPDATE kunden SET name=%s, address=%s, email=%s, phone=%s, password=%s WHERE id = %s",
            (self.name, self.address, self.email, self.phone, self.password, self.id)
        )

        Storage.execute_query(
            "UPDATE firmenkunden SET company_number = %s WHERE id = %s",
            (self.company_number, self.id)
        )

    @staticmethod
    def delete_customer(db_kunde_id):
        Storage.execute_query("DELETE FROM kunden WHERE id = %s", (db_kunde_id,))

    '''
    @staticmethod
    def load_customer_by_id(kunde_id):
        try:
            # اطلاعات پایه از جدول 'kunden'
            row = Storage.fetch_one(
                "SELECT * FROM kunden WHERE id = %s AND kundentyp = 'firma'", (kunde_id,)
            )
            if not row:
                return None

            _, name, address, email, phone, password, _ = row

            # اطلاعات اضافی از جدول 'firmenkunden'
            firm_row = Storage.fetch_one(
                "SELECT company_number FROM firmenkunden WHERE id = %s", (kunde_id,)
            )
            if not firm_row:
                return None

            kunde = Firmenkunde(name, address, email, phone, password, firm_row[0])
            kunde.id = kunde_id  # انتساب شناسه
            return kunde

        except DatenbankFehler as e:
            print("Fehler beim Laden des Firmenkunden:", e)
            return None
            
            
            
   @staticmethod
    def edit_customer(kunde_id, name, address, email, phone, password, company_number):
        try:
            # Update in main table
            query1 = """
                UPDATE kunden
                SET name = %s, address = %s, email = %s, phone = %s, password = %s
                WHERE id = %s
            """
            Storage.execute_query(query1, (name, address, email, phone, password, kunde_id))
    
            # Update in sub-table
            query2 = "UPDATE firmenkunden SET company_number = %s WHERE id = %s"
            Storage.execute_query(query2, (company_number, kunde_id))
    
            print(f"Firmenkunde mit ID {kunde_id} wurde aktualisiert.")
        except SpeicherFehler as e:
            print("Fehler beim Aktualisieren des Firmenkunden:", e)
         
    '''