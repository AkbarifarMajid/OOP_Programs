from produkte.produkt import Produkt

class Warenkorb:
    def __init__(self, kunde):
        self.kunde = kunde
        self.produkte = []
        self.gesamtsumme = 0


    def produkt_hinzufuegen(self, produkt: Produkt):
        self.produkte.append(produkt)
        self._berechne_gesamt()

    def produkt_entfernen(self, produkt: Produkt):
        if produkt in self.produkte:
            self.produkte.remove(produkt)
            self._berechne_gesamt()

    def warenkorb_leeren(self):
        self.produkte.clear()
        self.gesamtsumme = 0

    def _berechne_gesamt(self):
        self.gesamtsumme = sum(p.price for p in self.produkte)


    def __str__(self):
        beschreibung = f"Warenkorb für: {self.kunde.name}\n"
        beschreibung += "Produkte:\n"
        for p in self.produkte:
            beschreibung += f"- {p.name}: {p.price} €\n"
        beschreibung += f"Gesamtsumme: {round(self.gesamtsumme, 2)} €"
        return beschreibung
