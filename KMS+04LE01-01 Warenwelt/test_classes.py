from kunde import kunden_list,Kunde
from privatkunde import Privatkunde
from firmenkunde import Firmenkunde

kunde3 = Firmenkunde("IT Solutöäöäions GmbH", "Graz bei Garz 8073", "office@itsol.at", "+436601100000", "firmpass", "12345678")
kunde3.create()
print(kunde3.get_info())



kunde1 = Kunde("Majid", "Feldkirchen bei Garz 8073", "majid@test.com", "+436601112233", "1234")
kunde1.create()
kunde2 = Kunde("Maryam Jalali", "Felöääöädkirchen bei Garz 8073", "majid@test.com", "+436601112233", "1234")
kunde2.create()

kunde3 = Privatkunde("Sarah", "Linz reett 22001", "sarah@test.at", "+436601112211", "pass123", "10.03.2000")
kunde3.create()

print(kunde3.get_info())
print("Alter:", kunde3.berechne_alter(), "Jahre")




# Alle Kunden anzeigen
Kunde.get_all()


print("Aktuelle Kundenliste:")
for k in kunden_list:
    print(f"{k.id} - {k.name}")



# Kunde aktualisieren
Kunde.update(1,"email","maryam.neu@test.com")
Kunde.update(1,"name", "Maryam Azizi")
Kunde.update(1,"telefon", "+436601234567")


# Überprüfen ob Änderungen funktioniert haben
for k in kunden_list:
    print(f"{k.id} - {k.name}, {k.email}, {k.telefon}")



# Kunde löschen
Kunde.delete(1)

# Liste überprüfen
print("Aktuelle Kundenliste:")
for k in kunden_list:
    print(f"{k.id} - {k.name}")

# Alle Kunden anzeigen
Kunde.get_all()