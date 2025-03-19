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
        return f"{self.name} | {self.email} | Firmenkunde"

    @staticmethod
    def create_customer(name, address, email, phone, password, company_number):
        try:
            # اعتبارسنجی: با ساخت شیء Firmenkunde → فقط برای کنترل صحت ورودی
            _ = Firmenkunde(name, address, email, phone, password, company_number)

            # ذخیره در جدول اصلی
            query1 = """
                INSERT INTO kunden (name, address, email, phone, password, kundentyp)
                VALUES (%s, %s, %s, %s, %s, 'firma')
            """
            kunde_id = Storage.insert_and_get_id(query1, (name, address, email, phone, password))

            # ذخیره در جدول فرعی
            query2 = "INSERT INTO firmenkunden (id, company_number) VALUES (%s, %s)"
            Storage.execute_query(query2, (kunde_id, company_number))

            return kunde_id

        except (ValueError, SpeicherFehler) as e:
            print("Fehler beim Erstellen des Firmenkunden:", e)
            return None

    @staticmethod
    def get_all_firmen():
        try:
            return Storage.fetch_all("SELECT * FROM firmenkunden")
        except DatenbankFehler as e:
            print("Fehler beim Laden der Firmenkunden:", e)
            return None

    @staticmethod
    def get_firma_by_id(kunde_id):
        try:
            return Storage.fetch_one("SELECT * FROM firmenkunden WHERE id = %s", (kunde_id,))
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
                "UPDATE firmenkunden SET company_number = %s WHERE id = %s",
                (self.company_number, self.id)
            )

        except SpeicherFehler as e:
            print("Fehler beim Aktualisieren des Firmenkunden:", e)

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
    '''