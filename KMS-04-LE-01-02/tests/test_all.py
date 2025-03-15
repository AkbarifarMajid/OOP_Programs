# Standard Libraries
from datetime import datetime

# Exceptions
from storage.exceptions import (
    SpeicherFehler,
    VerbindungsFehler
)

# Core
from storage.storage import Storage

# Kunden (Customers)
from kunden.privatkunde import Privatkunde
from kunden.firmenkunde import Firmenkunde

# Produkte (Products)
from produkte.buch import Buch
from produkte.elektronik import Elektronik
from produkte.kleidung import Kleidung

def main():
    try:
        db = Storage()
        db.connect()
        db.create_tables()

        # ================================
        # ⛔ بخش زیر برای افزودن مشتری و محصول موقتاً غیرفعال شده اس
        #
        # print("\nNeue Kunden werden gespeichert...")
        # kunden_liste = [
        #     Privatkunde("Ali", "Tehran", "ali@example.com", "+989123456789", "ali123", "1995-03-15"),
        #     Privatkunde("Nina", "Wien", "nina@mail.at", "+4312345678", "nina456", "1988-07-22"),
        #     Firmenkunde("GreenTech AG", "München", "info@greentech.de", "+4989123456", "greentech!", "11223344"),
        #     Firmenkunde("CodeCloud GmbH", "Köln", "contact@codecloud.com", "+492211234567", "codecloud", "55667788")
        # ]
        #
        # for kunde in kunden_liste:
        #     db.save_customer(kunde)
        #
        # print("\nNeue Produkte werden gespeichert...")
        # produkt_liste = [
        #     Buch("Clean Code", 35.0, 0.8, "Robert C. Martin", 464),
        #     Buch("Der kleine Prinz", 12.5, 0.3, "Antoine de Saint-Exupéry", 96),
        #     Elektronik("Smartphone", 699.99, 0.4, "Samsung", 2),
        #     Elektronik("Bluetooth-Kopfhörer", 89.90, 0.2, "Sony", 1),
        #     Kleidung("Winterjacke", 149.99, 1.2, "L", "Schwarz"),
        #     Kleidung("Sneakers", 79.50, 0.9, "42", "Weiß")
        # ]
        #
        # for produkt in produkt_liste:
        #     db.save_product(produkt)
        #
        # print("\nBewertungen werden hinzugefügt...")
        # db.add_review_to_product(1, 5)
        # db.add_review_to_product(1, 4)
        # db.add_review_to_product(2, 3)
        # db.add_review_to_product(3, 5)
        # db.add_review_to_product(3, 4)
        # db.add_review_to_product(4, 2)
        # db.add_review_to_product(5, 4)
        # db.add_review_to_product(6, 5)
        # db.add_review_to_product(6, 5)

        # ================================
        # 🗑️ حذف مشتری و محصول
        #print("\n🗑️ Lösche einen Kunden und ein Produkt...")
        #db.delete_customer(1)
        #db.delete_product(1)

        # 📋 نمایش مشتری‌ها بعد از حذف
        print("\nVerbleibende Kunden nach dem Löschen:")
        kunden = db.load_all_customers()
        for k in kunden:
            print("------------------")
            print(k)

        # 📋 نمایش محصولات بعد از حذف
        print("\nVerbleibende Produkte nach dem Löschen:")
        produkte = db.load_all_products_with_rating()
        for p in produkte:
            print("------------------")
            print(p)
            avg = round(p.average_rating(), 2)
            print("Durchschnittsbewertung:", avg)

        db.close()
        print("\nErweiterter Test erfolgreich abgeschlossen.")

    except VerbindungsFehler as ve:
        print("Verbindungsfehler:", ve)
    except SpeicherFehler as se:
        print("Speicherfehler:", se)
    except Exception as e:
        print("Allgemeiner Fehler:", e)

if __name__ == "__main__":
    main()
