# Standard Libraries
from datetime import date

# Third-Party Libraries
import mysql.connector
from mysql.connector import Error

# Custom Exceptions
from storage.exceptions import (
    DatenbankFehler,
    VerbindungsFehler,
    SpeicherFehler,
    NichtGefundenFehler
)

# Kundenklassen (Customer Classes)
from kunden.kunde import Kunde
from kunden.privatkunde import Privatkunde
from kunden.firmenkunde import Firmenkunde

#  Produktklassen (Product Classes)
from produkte.buch import Buch
from produkte.elektronik import Elektronik
from produkte.kleidung import Kleidung


class Storage:
    # Constructor: Initialize the connection and cursor as None
    def __init__(self):
        self.conn = None
        self.cursor = None

    # Connect to MySQL database
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Akbarifar6503",
                database="online_shop_warenwelt_2"
            )
            self.cursor = self.conn.cursor()
            print("✅ Verbindung zur Datenbank erfolgreich!")
        except mysql.connector.Error:
            raise VerbindungsFehler()

    # Close the database connection
    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Verbindung geschlossen.")

    # Create all necessary tables: customers, products, sub-tables, reviews
    def create_tables(self):
        try:
            # جدول مشتری اصلی
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS kunden (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    address VARCHAR(255),
                    email VARCHAR(255),
                    phone VARCHAR(20),
                    password VARCHAR(255),
                    kundentyp VARCHAR(20)
                )
            """)

            # جدول مشتری خصوصی
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS privatkunden (
                    id INT PRIMARY KEY,
                    birthdate DATE,
                    FOREIGN KEY (id) REFERENCES kunden(id) ON DELETE CASCADE
                )
            """)

            # جدول مشتری شرکتی
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS firmenkunden (
                    id INT PRIMARY KEY,
                    company_number VARCHAR(20),
                    FOREIGN KEY (id) REFERENCES kunden(id) ON DELETE CASCADE
                )
            """)

            # جدول محصولات عمومی
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS produkte (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    price FLOAT,
                    weight FLOAT,
                    kategorie VARCHAR(50)
                )
            """)

            # جدول کتاب‌ها
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS produkte_buch (
                    id INT PRIMARY KEY,
                    author VARCHAR(255),
                    pages_count INT,
                    FOREIGN KEY (id) REFERENCES produkte(id) ON DELETE CASCADE
                )
            """)

            # جدول الکترونیک
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS produkte_elektronik (
                    id INT PRIMARY KEY,
                    brand VARCHAR(255),
                    warranty_years INT,
                    FOREIGN KEY (id) REFERENCES produkte(id) ON DELETE CASCADE
                )
            """)

            # جدول پوشاک
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS produkte_kleidung (
                    id INT PRIMARY KEY,
                    size VARCHAR(10),
                    color VARCHAR(50),
                    FOREIGN KEY (id) REFERENCES produkte(id) ON DELETE CASCADE
                )
            """)

            # جدول امتیازها - فقط به جدول produkte وصل می‌شود
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS bewertungen (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    produkt_id INT,
                    rating INT,
                    FOREIGN KEY (produkt_id) REFERENCES produkte(id) ON DELETE CASCADE
                )
            """)

            self.conn.commit()
            print("Alle Tabellen wurden erfolgreich erstellt.")

        except mysql.connector.Error:
            raise SpeicherFehler()

    # Save a customer (base + sub-table if Privatkunde or Firmenkunde)
    def save_customer(self, kunde):
        try:
            # مرحله 1: تعیین نوع مشتری
            kundentyp = "basis"
            if isinstance(kunde, Privatkunde):
                kundentyp = "privat"
            elif isinstance(kunde, Firmenkunde):
                kundentyp = "firma"

            # مرحله 2: درج اطلاعات عمومی در جدول `kunden`
            sql = """
                INSERT INTO kunden (name, address, email, phone, password, kundentyp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                kunde.name,
                kunde.address,
                kunde.email,
                kunde.phone,
                kunde.password,
                kundentyp
            )

            self.cursor.execute(sql, values)
            self.conn.commit()

            # گرفتن ID مشتری تازه درج‌شده
            kunde_id = self.cursor.lastrowid
            kunde._id = kunde_id  # برای استفاده در برنامه

            # مرحله 3: درج اطلاعات خاص در جدول فرعی
            if kundentyp == "privat":
                self.cursor.execute(
                    "INSERT INTO privatkunden (id, birthdate) VALUES (%s, %s)",
                    (kunde_id, kunde.birthdate)
                )
            elif kundentyp == "firma":
                self.cursor.execute(
                    "INSERT INTO firmenkunden (id, company_number) VALUES (%s, %s)",
                    (kunde_id, kunde.company_number)
                )

            self.conn.commit()
            print("Kunde erfolgreich gespeichert!")

        except mysql.connector.Error:
            raise SpeicherFehler()

    # Load all customers (base + sub-table data if needed)
    def load_all_customers(self):
        kunden = []
        try:
            self.cursor.execute("SELECT * FROM kunden")
            rows = self.cursor.fetchall()

            for row in rows:
                id_, name, address, email, phone, password, kundentyp = row

                if kundentyp == "privat":
                    self.cursor.execute("SELECT birthdate FROM privatkunden WHERE id = %s", (id_,))
                    result = self.cursor.fetchone()
                    if result:
                        birthdate = str(result[0])  # تبدیل به str برای کلاس
                        kunde = Privatkunde(name, address, email, phone, password, birthdate)
                        kunde._id = id_
                        kunden.append(kunde)

                elif kundentyp == "firma":
                    self.cursor.execute("SELECT company_number FROM firmenkunden WHERE id = %s", (id_,))
                    result = self.cursor.fetchone()
                    if result:
                        company_number = result[0]
                        kunde = Firmenkunde(name, address, email, phone, password, company_number)
                        kunde._id = id_
                        kunden.append(kunde)

                else:
                    kunde = Kunde(name, address, email, phone, password)
                    kunde._id = id_
                    kunden.append(kunde)

            return kunden

        except mysql.connector.Error:
            raise DatenbankFehler()

    # Save a product (base + specific type table: Buch, Elektronik, Kleidung)
    def save_product(self, produkt):
        try:
            # مرحله 1: تشخیص نوع محصول
            if isinstance(produkt, Buch):
                kategorie = "buch"
            elif isinstance(produkt, Elektronik):
                kategorie = "elektronik"
            elif isinstance(produkt, Kleidung):
                kategorie = "kleidung"
            else:
                kategorie = "unbekannt"

            # مرحله 2: درج در جدول پایه produkte
            sql = """
                INSERT INTO produkte (name, price, weight, kategorie)
                VALUES (%s, %s, %s, %s)
            """
            values = (
                produkt.name,
                produkt.price,
                produkt.weight,
                kategorie
            )
            self.cursor.execute(sql, values)
            self.conn.commit()

            produkt_id = self.cursor.lastrowid
            produkt._id = produkt_id  # تنظیم ID برای برنامه

            # مرحله 3: درج اطلاعات اختصاصی در جدول فرعی
            if kategorie == "buch":
                self.cursor.execute("""
                    INSERT INTO produkte_buch (id, author, pages_count)
                    VALUES (%s, %s, %s)
                """, (produkt_id, produkt.author, produkt.pages_count))

            elif kategorie == "elektronik":
                self.cursor.execute("""
                    INSERT INTO produkte_elektronik (id, brand, warranty_years)
                    VALUES (%s, %s, %s)
                """, (produkt_id, produkt.brand, produkt.warranty_years))

            elif kategorie == "kleidung":
                self.cursor.execute("""
                    INSERT INTO produkte_kleidung (id, size, color)
                    VALUES (%s, %s, %s)
                """, (produkt_id, produkt.size, produkt.color))

            self.conn.commit()
            print("Produkt erfolgreich gespeichert!")

        except mysql.connector.Error :
            raise SpeicherFehler()

    # Load all products with their specific details (no ratings)
    def load_all_products(self):
        produkte = []
        try:
            self.cursor.execute("SELECT * FROM produkte")
            rows = self.cursor.fetchall()

            for row in rows:
                id_, name, price, weight, kategorie = row
                produkt = None

                if kategorie == "buch":
                    self.cursor.execute("SELECT author, pages_count FROM produkte_buch WHERE id = %s", (id_,))
                    data = self.cursor.fetchone()
                    if data:
                        produkt = Buch(name, price, weight, data[0], data[1])

                elif kategorie == "elektronik":
                    self.cursor.execute("SELECT brand, warranty_years FROM produkte_elektronik WHERE id = %s", (id_,))
                    data = self.cursor.fetchone()
                    if data:
                        produkt = Elektronik(name, price, weight, data[0], data[1])

                elif kategorie == "kleidung":
                    self.cursor.execute("SELECT size, color FROM produkte_kleidung WHERE id = %s", (id_,))
                    data = self.cursor.fetchone()
                    if data:
                        produkt = Kleidung(name, price, weight, data[0], data[1])

                if produkt:
                    produkt._id = id_  # اختصاص ID از دیتابیس
                    produkte.append(produkt)

            return produkte

        except mysql.connector.Error:
            raise DatenbankFehler()

    # Add a review (rating) to a product
    def add_review_to_product(self, produkt_id, rating):
        try:
            # اعتبارسنجی امتیاز
            if not (1 <= rating <= 5):
                raise ValueError("Bewertung muss zwischen 1 und 5 liegen.")

            sql = """
                INSERT INTO bewertungen (produkt_id, rating)
                VALUES (%s, %s)
            """
            self.cursor.execute(sql, (produkt_id, rating))
            self.conn.commit()
            print(f"Bewertung {rating} für Produkt {produkt_id} wurde gespeichert.")

        except mysql.connector.Error:
            raise SpeicherFehler()

        except ValueError as ve:
            print(ve)

    # Calculate and return the average rating of a product
    def get_average_rating(self, produkt_id):
        try:
            self.cursor.execute("SELECT AVG(rating) FROM bewertungen WHERE produkt_id = %s", (produkt_id,))
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0

        except mysql.connector.Error:
            raise DatenbankFehler()

    # Load one product by ID, including ratings
    def load_product_with_rating(self, produkt_id):
        try:
            self.cursor.execute("SELECT * FROM produkte WHERE id = %s", (produkt_id,))
            row = self.cursor.fetchone()

            if not row:
                raise NichtGefundenFehler()


            id_, name, price, weight, kategorie = row

            # خواندن اطلاعات خاص
            if kategorie == "buch":
                self.cursor.execute("SELECT author, pages_count FROM produkte_buch WHERE id = %s", (id_,))
                data = self.cursor.fetchone()
                if data:
                    from produkte.buch import Buch
                    produkt = Buch(name, price, weight, data[0], data[1])

            elif kategorie == "elektronik":
                self.cursor.execute("SELECT brand, warranty_years FROM produkte_elektronik WHERE id = %s", (id_,))
                data = self.cursor.fetchone()
                if data:
                    from produkte.elektronik import Elektronik
                    produkt = Elektronik(name, price, weight, data[0], data[1])

            elif kategorie == "kleidung":
                self.cursor.execute("SELECT size, color FROM produkte_kleidung WHERE id = %s", (id_,))
                data = self.cursor.fetchone()
                if data:
                    from produkte.kleidung import Kleidung
                    produkt = Kleidung(name, price, weight, data[0], data[1])
            else:

                raise NichtGefundenFehler(f" Unbekannte Produktkategorie: {kategorie}")

            produkt._id = id_

            # بارگذاری امتیازها
            self.cursor.execute("SELECT rating FROM bewertungen WHERE produkt_id = %s", (id_,))
            ratings = self.cursor.fetchall()
            produkt.reviews = [r[0] for r in ratings]

            return produkt

        except mysql.connector.Error:
            raise DatenbankFehler()

    # Load all products, including their reviews
    def load_all_products_with_rating(self):
        produkte = []
        try:
            self.cursor.execute("SELECT * FROM produkte")
            rows = self.cursor.fetchall()

            for row in rows:
                id_, name, price, weight, kategorie = row

                produkt = None

                if kategorie == "buch":
                    self.cursor.execute("SELECT author, pages_count FROM produkte_buch WHERE id = %s", (id_,))
                    details = self.cursor.fetchone()
                    if details:
                        produkt = Buch(name, price, weight, details[0], details[1])

                elif kategorie == "elektronik":
                    self.cursor.execute("SELECT brand, warranty_years FROM produkte_elektronik WHERE id = %s", (id_,))
                    details = self.cursor.fetchone()
                    if details:
                        produkt = Elektronik(name, price, weight, details[0], details[1])

                elif kategorie == "kleidung":
                    self.cursor.execute("SELECT size, color FROM produkte_kleidung WHERE id = %s", (id_,))
                    details = self.cursor.fetchone()
                    if details:
                        produkt = Kleidung(name, price, weight, details[0], details[1])

                # تنظیم ID و افزودن به لیست
                if produkt:
                    produkt._id = id_
                    produkte.append(produkt)

            return produkte
        except mysql.connector.Error:
            raise DatenbankFehler()

    def delete_customer(self, kunde_id):
        try:
            self.cursor.execute("DELETE FROM kunden WHERE id = %s", (kunde_id,))
            self.conn.commit()
            print(f" Kunde mit ID {kunde_id} wurde gelöscht.")
        except mysql.connector.Error:
            raise SpeicherFehler()

    def delete_product(self, produkt_id):
        try:
            self.cursor.execute("DELETE FROM produkte WHERE id = %s", (produkt_id,))
            self.conn.commit()
            print(f"Produkt mit ID {produkt_id} wurde gelöscht.")
        except mysql.connector.Error:
            raise SpeicherFehler()
