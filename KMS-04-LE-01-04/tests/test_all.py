from tests import Privatkunde, Firmenkunde, Buch, Elektronik, Kleidung, Storage, SpeicherFehler, VerbindungsFehler


def main():
    try:


        '''
        # Test: Bewertung für ein Buch
        print("\nTest: Bewertung für Buch (ID=1)")
        buch = Buch.get_book_by_id(1)
        if buch:
            buch.add_review(5)
            buch.add_review(4)
            avg = buch.average_rating()
            print(f"Buch: {buch.name} | Ø Bewertung: {round(avg, 2)}")
        else:
            print("Buch nicht gefunden.")

        # Test: Bewertung für Elektronik
        print("\nTest: Bewertung für Elektronik (ID=4)")
        elektro = Elektronik.get_electronic_by_id(4)
        if elektro:
            elektro.add_review(4)
            elektro.add_review(3)
            avg = elektro.average_rating()
            print(f"Gerät: {elektro.name} | Ø Bewertung: {round(avg, 2)}")
        else:
            print("Elektronik nicht gefunden.")

        # Test: Bewertung für Kleidung
        print("\nTest: Bewertung für Kleidung (ID=7)")
        kleid = Kleidung.get_clothing_by_id(7)
        if kleid:
            kleid.add_review(5)
            kleid.add_review(5)
            avg = kleid.average_rating()
            print(f"Kleidung: {kleid.name} | Ø Bewertung: {round(avg, 2)}")
        else:
            print("Kleidungsstück nicht gefunden.")
        '''





        '''
        #--- Test: ADD Costumer

        kunde_id = Firmenkunde.create_customer(
            "ztzrz tzrzr", "dfgdg gfdfgfdg ", "",
            "+989123456789", "", "56564"
        )
        print("Neuer Privatkunde wurde gespeichert. ID:", kunde_id)
        '''


        '''   
        #--- Test: Show All Costumer

        firmen = Firmenkunde.get_all_firmen()
        print(firmen)

        # --Test Show all Costumer (2)
        print("\n Alle Firmenkunden ...")
        firmen = Firmenkunde.get_all_firmen()

        if firmen:
            for firma in firmen:
                print("-> ", firma)
        else:
            print("Gibt es keine Kunden")
        '''



        ''''
        # ---------------------
        #--- Test: Show bei ID Costumer
        
        kunde = Firmenkunde.get_firma_by_id(20)
        print(kunde)

        kunde2 = Privatkunde.get_privat_by_id(23)
        print(kunde2)
        '''

        '''
        #--- Test: Edit Costumer
       
        kunde = Firmenkunde.load_customer_by_id(20)
        if kunde:
            kunde.address = "Das ist neu Address Neue "
            kunde.edit_customer()
            print("Änderungen gespeichert.")
        '''


        '''
        # --- Test: Delete Costumer

        Firmenkunde.delete_customer(20)
        print("Kunde wurde gelöscht.")
        '''



        # ====================    TEST PRODUKT  =======================
        '''
        # ------ Test Elektronik ----------------
        print("\n Alle Elektronik Gräte:")
        elektroniks = Elektronik.get_all_electronics()
        if elektroniks:
            for e in elektroniks:
                print("-> ", e)
        else:
            print("Gibt es Keine Elektronik Gräte.")

        
        print("\n Lade Elektronik mit ID:")
        elektro = Elektronik.get_electronic_by_id(4)
        if elektro:
            print("* ", elektro)
        else:
            print("Kein Gerät mit dieser ID gefunden.")

        # ================================
        #----------  Test Kleidung ----------
        print("\nAlle Kleidung Sachen:")
        kleidungs = Kleidung.get_all_clothing()
        if kleidungs:
            for k in kleidungs:
                print("+ ", k)
        else:
            print("Keine Kleidung gefunden.")

        print("\nLade Kleidung mit ID :")
        kleid = Kleidung.get_clothing_by_id(9)
        if kleid:
            print("* ", kleid)
        else:
            print("Kein Kleidungsstück mit dieser ID gefunden.")
        '''


        '''
        # ------ Test Buch -----------------
        print("\nAlle Bücher ")
        books = Buch.get_all_books()

        if books:
            for book in books:
                print(book)
        else:
            print(" Keine Bücher gefunden oder Fehler beim Laden.")


        # --------------------------------------
        # Test: Ein Buch mit bestimmter ID laden
        print("\n Lade Buch mit ID :")

        buch_daten = Buch.get_book_by_id(1)

        if buch_daten:
            print(" Buchdaten:", buch_daten)
        else:
            print(" Kein Buch mit dieser ID gefunden.")
        '''


    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    main()