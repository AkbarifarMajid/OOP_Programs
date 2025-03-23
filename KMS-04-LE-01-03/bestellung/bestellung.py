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
        self.lieferart = lieferart  # فقط برای محاسبه، ذخیره نمی‌کنیم
        self.bestellzeitpunkt = datetime.now()
        self.gesamtbetrag = self.berechne_gesamtbetrag()



    def berechne_gesamtbetrag(self):
        # قیمت اولیه محصولات
        gesamt = sum(p.price for p in self.produkte)

        # اعمال تخفیف ۵٪ برای Firmenkunde
        if isinstance(self.kunde, Firmenkunde):
            gesamt *= 0.95

        # محاسبه هزینه‌ی ارسال
        versand = VersandService(self.produkte)
        versandkosten = versand.berechne_versandkosten(self.lieferart)

        # جمع نهایی
        gesamt += versandkosten
        return round(gesamt, 2)

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
                INSERT INTO bestellpositionen (bestell_id, produkt_id, preis)
                VALUES (%s, %s, %s)
                """,
                (bestell_id, produkt.id, produkt.price)
            )

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
