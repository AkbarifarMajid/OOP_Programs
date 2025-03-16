# Standard Libraries
from datetime import date

# Third-Party Libraries
import mysql.connector
from mysql.connector import Error

# -------------- Custom Modules------------

# Exceptions
from storage.exceptions import (
    DatenbankFehler,
    VerbindungsFehler,
    SpeicherFehler,
    NichtGefundenFehler
)

# Kundenklassen
from kunden.kunde import Kunde
from kunden.privatkunde import Privatkunde
from kunden.firmenkunde import Firmenkunde

# Produktklassen
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
            print(" *** Connected ***")
        except mysql.connector.Error:
            raise VerbindungsFehler()

    # Close the database connection
    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Connection lost !!!")

    # Create all necessary tables: customers, products, sub-tables, reviews
    def create_tables(self):
        try:
            # A dictionary of table creation SQL commands
            tables = {
                "kunden": """
                    CREATE TABLE IF NOT EXISTS kunden (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        address VARCHAR(255),
                        email VARCHAR(255),
                        phone VARCHAR(20),
                        password VARCHAR(255),
                        kundentyp VARCHAR(20)
                    )
                """,

                "privatkunden": """
                    CREATE TABLE IF NOT EXISTS privatkunden (
                        id INT PRIMARY KEY,
                        birthdate DATE,
                        FOREIGN KEY (id) REFERENCES kunden(id) ON DELETE CASCADE
                    )
                """,

                "firmenkunden": """
                    CREATE TABLE IF NOT EXISTS firmenkunden (
                        id INT PRIMARY KEY,
                        company_number VARCHAR(20),
                        FOREIGN KEY (id) REFERENCES kunden(id) ON DELETE CASCADE
                    )
                """,

                "produkte": """
                    CREATE TABLE IF NOT EXISTS produkte (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        price FLOAT,
                        weight FLOAT,
                        kategorie VARCHAR(50)
                    )
                """,

                "produkte_buch": """
                    CREATE TABLE IF NOT EXISTS produkte_buch (
                        id INT PRIMARY KEY,
                        author VARCHAR(255),
                        pages_count INT,
                        FOREIGN KEY (id) REFERENCES produkte(id) ON DELETE CASCADE
                    )
                """,

                "produkte_elektronik": """
                    CREATE TABLE IF NOT EXISTS produkte_elektronik (
                        id INT PRIMARY KEY,
                        brand VARCHAR(255),
                        warranty_years INT,
                        FOREIGN KEY (id) REFERENCES produkte(id) ON DELETE CASCADE
                    )
                """,

                "produkte_kleidung": """
                    CREATE TABLE IF NOT EXISTS produkte_kleidung (
                        id INT PRIMARY KEY,
                        size VARCHAR(10),
                        color VARCHAR(50),
                        FOREIGN KEY (id) REFERENCES produkte(id) ON DELETE CASCADE
                    )
                """,

                "bewertungen": """
                    CREATE TABLE IF NOT EXISTS bewertungen (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        produkt_id INT,
                        rating INT,
                        FOREIGN KEY (produkt_id) REFERENCES produkte(id) ON DELETE CASCADE
                    )
                """
            }

            for table_name, sql in tables.items():
                self.cursor.execute(sql)

            # Save changes to the database
            self.conn.commit()
            print("All tables were successfully created.")

        except mysql.connector.Error :
            raise SpeicherFehler()

    #------------------------------- Client methods -------------------------------------

    # Save a customer (base + sub-table if Privatkunde or Firmenkunde)
    def save_customer(self, kunde):
        try:
            # Step 1: Detect customer type
            kundentyp = "basis"
            if isinstance(kunde, Privatkunde):
                kundentyp = "privat"
            elif isinstance(kunde, Firmenkunde):
                kundentyp = "firma"

            # Step 2: Insert basic customer data into 'kunden' table
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

            #  Get the generated customer ID
            db_kunde_id = self.cursor.lastrowid
            kunde._id = db_kunde_id

            # Step 3: Insert type-specific info into corresponding sub-table
            if kundentyp == "privat":
                self.cursor.execute(
                    "INSERT INTO privatkunden (id, birthdate) VALUES (%s, %s)",
                    (db_kunde_id, kunde.birthdate)
                )
            elif kundentyp == "firma":
                self.cursor.execute(
                    "INSERT INTO firmenkunden (id, company_number) VALUES (%s, %s)",
                    (db_kunde_id, kunde.company_number)
                )

            self.conn.commit()
            print("*** Customer successfully saved ***")

        except mysql.connector.Error:
            raise SpeicherFehler()

    # Delete a customer from the database using their ID
    def delete_customer(self, db_kunde_id):
        try:
            self.cursor.execute("DELETE FROM kunden WHERE id = %s", (db_kunde_id,))
            self.conn.commit()
            print(f"Customer with id {db_kunde_id} was deleted.")
        except mysql.connector.Error:
            raise SpeicherFehler()

    # Load all customers (base + sub-table data if needed) from database and return them as a list
    def load_all_customers(self):
        kunden = []

        try:
            # Step 1: Read all customers from the main table
            self.cursor.execute("SELECT * FROM kunden")
            rows = self.cursor.fetchall()

            for row in rows:
                db_kunde_id, name, address, email, phone, password, kundentyp = row

                if kundentyp == "privat":
                    self.cursor.execute("SELECT birthdate FROM privatkunden WHERE id = %s", (db_kunde_id,))
                    result = self.cursor.fetchone()
                    if result:
                        birthdate = str(result[0])
                        kunde = Privatkunde(name, address, email, phone, password, birthdate)

                elif kundentyp == "firma":
                    self.cursor.execute("SELECT company_number FROM firmenkunden WHERE id = %s", (db_kunde_id,))
                    result = self.cursor.fetchone()
                    if result:
                        company_number = result[0]
                        kunde = Firmenkunde(name, address, email, phone, password, company_number)

                else:
                    # Unknown or invalid customer type → raise exception
                    raise DatenbankFehler("Unknown customer type in the data record.")

                # Set customer ID and add to list
                kunde._id = db_kunde_id
                kunden.append(kunde)

            return kunden

        except mysql.connector.Error:
            raise DatenbankFehler()

#--------------------------------Product methods-------------------------------------
    # Save a product (base + specific type: Buch, Elektronik, Kleidung)
    def save_product(self, produkt):
        try:
            # Step 1: Determine product category
            if isinstance(produkt, Buch):
                kategorie = "buch"
            elif isinstance(produkt, Elektronik):
                kategorie = "elektronik"
            elif isinstance(produkt, Kleidung):
                kategorie = "kleidung"
            else:
                kategorie = "unbekannt"

            # Step 2: Insert into base table 'produkte'
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

            # Step 3: Get the product ID from database
            db_produkt_id = self.cursor.lastrowid
            produkt._id = db_produkt_id

            # Step 4: Insert into category-specific sub-table
            if kategorie == "buch":
                self.cursor.execute("""
                    INSERT INTO produkte_buch (id, author, pages_count)
                    VALUES (%s, %s, %s)
                """, (db_produkt_id, produkt.author, produkt.pages_count))

            elif kategorie == "elektronik":
                self.cursor.execute("""
                    INSERT INTO produkte_elektronik (id, brand, warranty_years)
                    VALUES (%s, %s, %s)
                """, (db_produkt_id, produkt.brand, produkt.warranty_years))

            elif kategorie == "kleidung":
                self.cursor.execute("""
                    INSERT INTO produkte_kleidung (id, size, color)
                    VALUES (%s, %s, %s)
                """, (db_produkt_id, produkt.size, produkt.color))

            self.conn.commit()
            print("*** Product successfully saved ***")

        except mysql.connector.Error:
            raise SpeicherFehler()

    # Load all products from the database (including specific details, no ratings)
    def load_all_products(self):
        produkte = []  # List to store loaded product objects

        try:
            # Step 1: Read all rows from 'produkte' table
            self.cursor.execute("SELECT * FROM produkte")
            rows = self.cursor.fetchall()

            for row in rows:
                db_produkt_id, name, price, weight, kategorie = row

                # Step 2: Check the category and load specific attributes
                if kategorie == "buch":
                    self.cursor.execute("SELECT author, pages_count FROM produkte_buch WHERE id = %s", (db_produkt_id,))
                    data = self.cursor.fetchone()
                    if data:
                        produkt = Buch(name, price, weight, data[0], data[1])

                elif kategorie == "elektronik":
                    self.cursor.execute("SELECT brand, warranty_years FROM produkte_elektronik WHERE id = %s",
                                        (db_produkt_id,))
                    data = self.cursor.fetchone()
                    if data:
                        produkt = Elektronik(name, price, weight, data[0], data[1])

                elif kategorie == "kleidung":
                    self.cursor.execute("SELECT size, color FROM produkte_kleidung WHERE id = %s", (db_produkt_id,))
                    data = self.cursor.fetchone()
                    if data:
                        produkt = Kleidung(name, price, weight, data[0], data[1])

                else:

                    raise DatenbankFehler(f"Unknown product category: {kategorie}")

                # Step 3: Assign database ID and add to list
                produkt._id = db_produkt_id
                produkte.append(produkt)

            return produkte

        except mysql.connector.Error:
            raise DatenbankFehler()

    def delete_product(self, produkt_id):
        try:
            self.cursor.execute("DELETE FROM produkte WHERE id = %s", (produkt_id,))
            self.conn.commit()
            print(f"Product with id {produkt_id} has been deleted.")
        except mysql.connector.Error:
            raise SpeicherFehler()

#-------------------------- Rating and uploading products with ratings --------------------------
    # Add a review (rating) to a product
    def add_review_to_product(self, db_produkt_id, rating):
        try:
            # Step 1: Validate rating
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")

            # Step 2: Insert rating into 'bewertungen' table
            sql = """
                INSERT INTO bewertungen (produkt_id, rating)
                VALUES (%s, %s)
            """
            self.cursor.execute(sql, (db_produkt_id, rating))
            self.conn.commit()

            print(f"Rating {rating} for Product {db_produkt_id} has been saved.")

        except mysql.connector.Error:
            raise SpeicherFehler()

        except ValueError as ve:
            print(ve)

    # Calculate and return the average rating of a product
    def get_average_rating(self, db_produkt_id):
        try:
            # Step 1: Run SQL query to calculate average rating
            self.cursor.execute(
                "SELECT AVG(rating) FROM bewertungen WHERE produkt_id = %s",
                (db_produkt_id,)
            )

            # Step 2: Fetch result
            result = self.cursor.fetchone()

            # Step 3: Check if result is not None
            if result[0] is not None:
                return result[0]
            else:
                return 0

        except mysql.connector.Error:
            raise DatenbankFehler()

    # Load one product by ID, including its ratings
    def load_product_with_rating(self, db_produkt_id):
        try:
            self.cursor.execute("SELECT * FROM produkte WHERE id = %s", (db_produkt_id,))
            row = self.cursor.fetchone()

            if not row:
                raise NichtGefundenFehler("Product not found.")

            db_produkt_id, name, price, weight, kategorie = row

            # Map of category -----> table name + class + columns
            details = {
                "buch": {
                    "table": "produkte_buch",
                    "class": Buch,
                    "columns": ("author", "pages_count")
                },
                "elektronik": {
                    "table": "produkte_elektronik",
                    "class": Elektronik,
                    "columns": ("brand", "warranty_years")
                },
                "kleidung": {
                    "table": "produkte_kleidung",
                    "class": Kleidung,
                    "columns": ("size", "color")
                }
            }

            if kategorie not in details:
                raise DatenbankFehler(f":Unknown product category {kategorie}")

            table = details[kategorie]["table"]
            klass = details[kategorie]["class"]
            cols = ", ".join(details[kategorie]["columns"])

            self.cursor.execute(f"SELECT {cols} FROM {table} WHERE id = %s", (db_produkt_id,))
            result = self.cursor.fetchone()

            if not result:
                raise NichtGefundenFehler(f"No details for product with ID {db_produkt_id}")

            # Create product object dynamically
            produkt = klass(name, price, weight, *result)
            produkt._id = db_produkt_id

            # Bewertungen laden (Liste von Zahlen)
            self.cursor.execute("SELECT rating FROM bewertungen WHERE produkt_id = %s", (db_produkt_id,))
            rows = self.cursor.fetchall()

            bewertungen = []
            for row in rows:
                bewertungen.append(row[0])
            produkt.reviews = bewertungen

            return produkt

        except mysql.connector.Error:
            raise DatenbankFehler()

    # Load all products including their average ratings
    def load_all_products_with_rating(self):
        produkte = []

        try:
            # Mapping category to table, columns, and class
            details_map = {
                "buch": {
                    "table": "produkte_buch",
                    "columns": ("author", "pages_count"),
                    "class": Buch
                },
                "elektronik": {
                    "table": "produkte_elektronik",
                    "columns": ("brand", "warranty_years"),
                    "class": Elektronik
                },
                "kleidung": {
                    "table": "produkte_kleidung",
                    "columns": ("size", "color"),
                    "class": Kleidung
                }
            }

            # Step 1: Get all base products
            self.cursor.execute("SELECT * FROM produkte")
            rows = self.cursor.fetchall()

            for row in rows:
                db_produkt_id, name, price, weight, kategorie = row

                # Step 2: Validate category and extract info
                if kategorie not in details_map:
                    raise DatenbankFehler(f"Unknown product category: {kategorie}")

                info = details_map[kategorie]
                table = info["table"]
                cols = ", ".join(info["columns"])
                klass = info["class"]

                # Step 3: Load specific details
                self.cursor.execute(f"SELECT {cols} FROM {table} WHERE id = %s", (db_produkt_id,))
                details = self.cursor.fetchone()

                if not details:
                    raise NichtGefundenFehler(f"Details missing for product ID {db_produkt_id}")

                # Step 4: Create product object and assign ID
                produkt = klass(name, price, weight, *details)
                produkt._id = db_produkt_id

                # Step 5: Load product reviews
                self.cursor.execute("SELECT rating FROM bewertungen WHERE produkt_id = %s", (db_produkt_id,))
                rows = self.cursor.fetchall()
                ratings = []
                for row in rows:
                    ratings.append(row[0])
                produkt.reviews = ratings

                produkte.append(produkt)

            return produkte

        except mysql.connector.Error:
            raise DatenbankFehler()

