from warenkorb.warenkorb import Warenkorb
from tests import Privatkunde, Firmenkunde, Buch, Elektronik, Kleidung, Storage, SpeicherFehler, VerbindungsFehler


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




    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    main()