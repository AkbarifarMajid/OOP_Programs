
from datetime import datetime

# Exceptions
from storage.exceptions import SpeicherFehler, VerbindungsFehler

# Core
from storage.storage import Storage

# Kunden
#from kunden.privatkunde import Privatkunde
#from kunden.firmenkunde import Firmenkunde
from kunden import Kunde, Privatkunde, Firmenkunde


# Produkte
#from produkte.buch import Buch
#from produkte.elektronik import Elektronik
#from produkte.kleidung import Kleidung
from produkte import Buch, Elektronik, Kleidung


from storage.exceptions import (
    VerbindungsFehler,
    SpeicherFehler,
    NichtGefundenFehler,
    DatenbankFehler
)
import mysql.connector

def main():
    try:
        db = Storage()
        db.connect()
        #db.create_tables()

        # Vorherige Daten löschen (nur im Testfall)
        #db.delete_all_data()
        '''
        # ================================
        #  Kunden speichern
        print("\n Kunden werden gespeichert...")
        kunden_liste = [
            Privatkunde("Majid Akbarifar", "Tehran", "majid@example.com", "+989123456000", "majid123", "1993-04-21"),
            Privatkunde("Nina Schneider", "Wien", "nina@mail.at", "+4312345678", "nina456", "1988-07-22"),
            Privatkunde("Ali Reza", "Shiraz", "ali.r@gmail.com", "+989123456789", "ali2024", "1990-01-15"),
            Privatkunde("Sara Müller", "Berlin", "sara.m@example.de", "+4930123456", "saraPass", "1992-05-30"),
            Privatkunde("David Kim", "Hamburg", "david.kim@gmail.com", "+4940123456", "kimPass", "1995-09-11"),
            Firmenkunde("GreenTech AG", "München", "info@greentech.de", "+4989123456", "greentech!", "11223344"),
            Firmenkunde("CodeCloud GmbH", "Köln", "contact@codecloud.com", "+492211234567", "codecloud", "55667788"),
            Firmenkunde("DataSoft GmbH", "Frankfurt", "info@datasoft.com", "+49691234567", "ds2024", "77889900"),
            Firmenkunde("SunSolar GmbH", "Stuttgart", "hello@sunsolar.com", "+49711234567", "solar2024", "33445566"),
            Firmenkunde("BlueNet AG", "Düsseldorf", "support@bluenet.de", "+492112345678", "bluepass", "88997766")
        ]

        for kunde in kunden_liste:
            db.save_customer(kunde)

        # ================================
        # Produkte speichern
        print("\n Produkte werden gespeichert...")
        produkt_liste = [
            Buch("Clean Code", 35.0, 0.8, "Robert C. Martin", 464),
            Buch("Der kleine Prinz", 12.5, 0.3, "Antoine de Saint-Exupéry", 96),
            Buch("Python Basics", 25.0, 0.7, "M. Akbarifar", 300),
            Elektronik("Smartphone", 699.99, 0.4, "Samsung", 2),
            Elektronik("Bluetooth-Kopfhörer", 89.90, 0.2, "Sony", 1),
            Elektronik("Laptop", 1200.0, 2.5, "Lenovo", 2),
            Kleidung("Winterjacke", 149.99, 1.2, "L", "Schwarz"),
            Kleidung("Sneakers", 79.50, 0.9, "42", "Weiß"),
            Kleidung("T-Shirt", 20.0, 0.3, "M", "Blau"),
            Kleidung("Hose", 49.90, 0.7, "XL", "Grau")
        ]

        for produkt in produkt_liste:
            db.save_product(produkt)

        # ================================
        #  Bewertungen hinzufügen
        print("\n Bewertungen hinzufügen...")
        db.add_review_to_product(1, 5)
        db.add_review_to_product(1, 4)
        db.add_review_to_product(2, 3)
        db.add_review_to_product(3, 4)
        db.add_review_to_product(4, 5)
        db.add_review_to_product(5, 4)
        db.add_review_to_product(6, 5)
        db.add_review_to_product(7, 3)
        db.add_review_to_product(8, 5)
        db.add_review_to_product(9, 4)

        # ================================
        #  Einzelnen Kunden laden
        print("\n Lade Kunden mit ID = 1:")
        kunde = db.load_customer_by_id(1)
        print(kunde)
        
        # Kunden aktualisieren
        print("\n Kunde mit ID = 1 wird aktualisiert...")
        kunde.address = "Isfahan"
        db.update_customer(kunde)
        print("Aktualisierter Kunde:", db.load_customer_by_id(1))
        '''
        #  Kunde löschen
        print("\n Lösche Kunde mit ID = 2...")
        db.delete_customer(2)

        #  Alle Kunden laden
        print("\n Alle verbleibenden Kunden:")
        kunden = db.load_all_customers()
        for kunde in kunden:
            print(f"ID: {kunde.id} -> Name{kunde.name}")


        # ================================
        #  Ein Produkt mit Bewertung laden
        print("\n Lade Produkt mit Bewertung (ID = 1):")
        produkt = db.load_product_with_rating(5)
        print(produkt)
        print("Durchschnittsbewertung:", produkt.average_rating())

        #  Alle Produkte mit Bewertung laden
        print("\n Alle Produkte mit Bewertung:")
        produkte = db.load_all_products_with_rating()
        for prod in produkte:
            print(f"ID: {prod.id} - {prod.name} --> " "Ø:", round(prod.average_rating(),2))

            #print("-", p.name, "| Ø:", round(p.average_rating(), 2))



        #-----SpeicherFehler: Daten mit ungültigem Feld
        '''
        try:
            print("\nTest SpeicherFehler (NULL-Feld)...")
            db.cursor.execute(
                "INSERT INTO kunden (name, address, email, phone, password, kundentyp) VALUES (%s,%s,%s,%s,%s,%s)",
                ("Test", None, "test@test.com", "123", "abc", "privat")) 
            db.conn.commit()
        except mysql.connector.Error:
            try:
                raise SpeicherFehler()
            except SpeicherFehler as e:
                print("!!! ", e)
        '''

        # NichtGefundenFehler: Kunde mit falscher ID
        '''
        try:
            print("\nTest NichtGefundenFehler (falsche ID)...")
            db.cursor.execute("SELECT * FROM kunden WHERE id = %s", (999999,))
            row = db.cursor.fetchone()
            if not row:
                raise NichtGefundenFehler()
        except NichtGefundenFehler as e:
            print("!!! ", e)
        '''


        '''
        #---DatenbankFehler: falscher SQL-Befehl
        try:
            print("\nTest DatenbankFehler (Syntaxfehler)...")
            db.cursor.execute("SELEC * FROM kunden")
        except mysql.connector.Error:
            try:
                raise DatenbankFehler()
            except DatenbankFehler as e:
                print("!!! ", e)
        '''



        #-----Verbindung schließen
        db.close()
        #print("\n Alle Tests erfolgreich abgeschlossen.")

    except VerbindungsFehler as ve:
        print("Verbindungsfehler:", ve)
    except SpeicherFehler as se:
        print("Speicherfehler:", se)
    except Exception as e:
        print("Allgemeiner Fehler:", e)


if __name__ == "__main__":
    main()
