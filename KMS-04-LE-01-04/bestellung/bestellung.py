from datetime import datetime
from storage.storage import Storage
from kunden.firmenkunde import Firmenkunde
from versand.versand_service import VersandService
from zahlung.zahlung import Zahlung


class Bestellung:
    def __init__(self, kunde, produkte, zahllung, lieferart="Standardversand"):
        self.kunde = kunde
        self.produkte = produkte
        self.zahllung = zahllung
        self.lieferart = lieferart
        self.bestellzeitpunkt = datetime.now()
        self.gesamt_anzahl = sum(getattr(p, "anzahl", 1) for p in self.produkte)
        self.versand = VersandService(self.produkte)
        self.versandkosten = self.versand.berechne_versandkosten(self.lieferart)


        self.berechne_gesamtbetrag()

    def berechne_gesamtbetrag(self):
        self.bruttosumme = sum(p.price * getattr(p, "anzahl", 1) for p in self.produkte)
        self.rabatt = 0


        if hasattr(self.kunde, "kundentyp") and self.kunde.kundentyp == "firma":
            self.rabatt = round(self.bruttosumme * 0.05, 2)

        self.gesamtbetrag = round(self.bruttosumme - self.rabatt, 2)


    def erstelle_rechnung(self):
        bestell_id = Storage.insert_and_get_id(
            """
            INSERT INTO bestellungen (kunde_id, bestellzeitpunkt, gesamtbetrag, zahllung_id)
            VALUES (%s, %s, %s, %s)
            """,
            (self.kunde.id, self.bestellzeitpunkt, self.gesamtbetrag, self.zahllung.id)
        )

        for produkt in self.produkte:
            Storage.execute_query(
                """
                INSERT INTO bestellpositionen (bestell_id, produkt_id, preis, anzahl)
                VALUES (%s, %s, %s, %s)
                """,
                (bestell_id, produkt.id, produkt.price, getattr(produkt, "anzahl", 1))
            )

        self.bestell_id = bestell_id
        return bestell_id

    def __str__(self):
        zeilen = [
            f" Bestellung von Kunde-ID {self.kunde.id}",
            f"Datum: {self.bestellzeitpunkt.strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        for p in self.produkte:
            zeilen.append(f" - {p.name}: {p.price} €")
        zeilen.append(f"Gesamtbetrag: {self.gesamtbetrag} €")
        return "\n".join(zeilen)
