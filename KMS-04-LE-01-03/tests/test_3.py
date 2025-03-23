
from tests import Privatkunde, Firmenkunde, Buch, Elektronik, Kleidung, Storage, SpeicherFehler, VerbindungsFehler,Warenkorb, Bestellung
from versand.versand_service import VersandService
from zahlung.zahlung import Zahlung

def main():
    try:

        '''
        buch = Buch.get_book_by_id(11)
        elek = Elektronik.get_electronic_by_id(4)

        kunde = Privatkunde.get_privat_by_id(1)

        #print(buch)
        #print(elek)
        #print(kunde)
        wk = Warenkorb(kunde)


        wk.produkt_hinzufuegen(buch)
        wk.produkt_hinzufuegen(elek)


        print("\n Inhalt des Warenkorbs:")
        print(wk)
        '''


        '''
        # ----------------------------
        print("\nTest: Alle Privatkunden laden...")
        privatkunden = Privatkunde.get_all_privat_kunde()

        if privatkunden:
            for k in privatkunden:
                print("+", k.name, "|", k.email)
        else:
            print(" Keine Privatkunden gefunden.")

        # ----------------------------
        print("\n Test: Alle Firmenkunden laden...")
        firmenkunden = Firmenkunde.get_all_firmen_kunde()

        if firmenkunden:
            for f in firmenkunden:
                print("*", f.name, "|", f.email)
        else:
            print("⚠ Keine Firmenkunden gefunden.")
        '''


        '''
        print("\n Test: Firmenkunde erstellen mit E-Mail-Prüfung")

        kunde_id = Firmenkunde.create_customer(
            name="Boba GmbH",
            address="Innovationstr. 42, Berlin",
            email="info@futuretech.de", 
            phone="+491771234567",
            password="ft2025",
            company_number="98765432"
        )

        if kunde_id:
            print(f" Firmenkunde erfolgreich erstellt. ID: {kunde_id}")
        else:
            print(" Kunde konnte nicht erstellt werden.")
        '''


        '''
        print("\n Test: Privatkunde erstellen mit E-Mail-Prüfung")

        kunde_id = Privatkunde.create_customer(
            name="Nima Rezaei",
            address="Wiener Straße 17, Linz",
            email="nima.rezaei@example.com",  
            phone="+4366011122233",
            password="nima2024",
            birthdate="1990-11-23"
        )

        if kunde_id:
            print(f"Privatkunde erfolgreich erstellt. ID: {kunde_id}")
        else:
            print(" Kunde konnte nicht erstellt werden.")

        '''


        '''
        #--------------------- Bestellung test ----------------
       
        print("\n Test: Bestellung erstellen...")

        #  Kunde laden
        kunde = Firmenkunde.get_firma_by_id(9)  # Stelle sicher, dass ID 1 existiert

        # 🛍 Produkte laden
        buch = Buch.get_book_by_id(13)
        elektro = Kleidung.get_clothing_by_id(10)

        #  Warenkorb erstellen und Produkte hinzufügen
        wk = Warenkorb(kunde)
        wk.produkt_hinzufuegen(buch)
        wk.produkt_hinzufuegen(elektro)

        # Zahlung
        zahlung = Zahlung("Kreditkarte")
        
        #  Bestellung erstellen (nur Produktliste wird übergeben)
        bestellung = Bestellung(kunde, wk.produkte, zahlung)

        #  Kontrolle vor dem Speichern
        print(" Produkt-IDs im Warenkorb:")
        print(f" Kunde-ID: {kunde.id}")
        for p in wk.produkte:
            print(f" - {p.name}, ID: {p.id}")

        #  Bestellung speichern
        rechnung = bestellung.erstelle_rechnung()

        #  Rückmeldung
        if rechnung:
            print("Bestellung erfolgreich gespeichert. Bestell-ID:", rechnung)
            print(bestellung)
        else:
            print(" Fehler beim Speichern der Bestellung.")
        '''


        # --------------------- Versand Test ----------------
        print("\nTest: Versandkosten berechnen...")


        kunde = Privatkunde.get_privat_by_id(3)
        elek1= Elektronik.get_electronic_by_id(5)
        elek2 = Elektronik.get_electronic_by_id(16)


        wk = Warenkorb(kunde)
        wk.produkt_hinzufuegen(elek1)
        wk.produkt_hinzufuegen(elek2)

        # Zahlung
        zahlung = Zahlung("Kreditkarte")
        zahlung.erstelle_zahllung()

        # Bestellung mit Versand
        lieferart = "Expressversand"
        bestellung = Bestellung(kunde, wk.produkte, zahlung, lieferart)



        # Rechnung erstellen
        bestell_id = bestellung.erstelle_rechnung()

        # Ausgabe
        print(f"\nBestellung erfolgreich gespeichert mit ID: {bestell_id}")
        print(bestellung)




    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    main()