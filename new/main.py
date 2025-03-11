from privatkunde import Privatkunde
from firmenkunde import Firmenkunde
from kunde import Kunde, kunden_list

def hauptmenue():
    while True:
        print("\n----- Hauptmenü -------")
        print("1. Privatkunde erstellen")
        print("2. Firmenkunde erstellen")
        print("3. Alle Kunden anzeigen")
        print("4. Kunde aktualisieren")
        print("5. Kunde löschen")
        print("0. Beenden")


        wahl = input("Bitte waehlen Sie eine Option: ")

        if wahl == "1":
            name = input("Name: ")
            adresse = input("Adresse: ")
            email = input("E-Mail: ")
            telefon = input("Telefon: ")
            passwort = input("Passwort: ")
            geburtsdatum = input("Geburtsdatum (dd.mm.yyyy): ")

            try:
                kunde = Privatkunde(name, adresse, email, telefon, passwort, geburtsdatum)
                kunde.create()
            except ValueError as e:
                print("!!!! ERROE Kunde !!!!!!",e)

        elif wahl == "2":
            name = input("Firmenname: ")
            adresse = input("Adresse: ")
            email = input("E-Mail: ")
            telefon = input("Telefon: ")
            passwort = input("Passwort: ")
            firmennummer = input("Firmennummer: ")

            try:
                kunde = Firmenkunde(name, adresse, email, telefon, passwort, firmennummer)
                kunde.create()
            except ValueError as e:
                print("!!!! ERROE FIRMA !!!!!!",e)
            
        elif wahl == "3":
            Kunde.get_all()

        elif wahl == "4":
            try:
                id = int(input("Kunden-ID zum Bearbeiten: "))
                feld = input("Feldname (name, adresse, email, telefon, passwort): ")
                neuer_wert = input("Neuer Wert: ")
                Kunde.update(id, feld, neuer_wert)
            except Exception as e:
                print(" Fehler Akualizieren:", e)

        elif wahl == "5":
            try:
                id = int(input("Kunden-ID zum Löschen: "))
                Kunde.delete(id)
            except Exception as e:
                print(" Fehler KUNDE loeschen:", e)

        elif wahl == "0":
            print("Programm beendet.")
            break

        else:
            print("Ungueltige Eingabe")

# Start des Programms
if __name__ == "__main__":
    hauptmenue()

