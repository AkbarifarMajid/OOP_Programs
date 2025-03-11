# -*- coding: utf-8 -*-

# Importing the classes
from produkt import Produkt
from kunde import Kunde
from bestellung import Bestellung
from zahlung import Zahlung

# Testen der Produktklasse
produkt1 = Produkt(1, "Laptop", 1000, "High-end Laptop")
produkt2 = Produkt(2, "Smartphone", 500, "Latest Model Smartphone")

produkt1.apply_discount(20)


kunde1 = Kunde(1, "Max Mustermann", "Musterstraße 1, 12345 Musterstadt", "max@example.com")
kunde1 = Kunde(2, "Majid akbarifar", "Mtrrrre 5646, 12345 Musterstadt", "max@example.com",vip_status = True)
kunde1.update_email("max.newemail@example.com")
print(kunde1.get_info())

bestellung1 = Bestellung(1, kunde1)
bestellung1.add_produkt(produkt1)
bestellung1.add_produkt(produkt2)

bestellung2 = Bestellung(2, kunde1)
bestellung2.add_produkt(produkt2)

print(bestellung1.get_bestellung_info())

print(bestellung1.calculate_total())
print("________________________________________")

print(bestellung2.get_bestellung_info())
print(bestellung2.calculate_total())