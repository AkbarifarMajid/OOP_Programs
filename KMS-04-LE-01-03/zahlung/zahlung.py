# zahlung/zahlung.py
from datetime import datetime
from storage.storage import Storage

class Zahlung:
    def __init__(self, method):
        # لیست روش‌های پرداخت ممکن
        self.methoden = ["Kreditkarte", "PayPal", "Rechnung"]
        self.method = method
        self.datum = datetime.now()
        self._id = None

    @property
    def id(self):
        return self._id if hasattr(self, "_id") else None

    @id.setter
    def id(self, value):
        self._id = value

    def erstelle_zahllung(self):

        self._id = Storage.insert_and_get_id(
            """
            INSERT INTO zahllung (zahllung_method,zahllung_datum)
            VALUES (%s, %s)
            """,
            (self.method, self.datum)
        )

    def get_alle_methoden(self):
        """
        Gibt alle verfügbaren Zahlungsmethoden zurück.
        """
        return self.methoden

    def methode_waehlen(self, auswahl_index: int):
        """
        Wählt eine Zahlungsmethode anhand des Index (1-basiert).
        """
        if 1 <= auswahl_index <= len(self.methoden):
            self.gewaehlte_methode = self.methoden[auswahl_index - 1]
            return self.gewaehlte_methode
        else:
            raise ValueError("Ungültige Auswahl für Zahlungsmethode.")

    def __str__(self):
        return f"Zahlungsmethode: {self.gewaehlte_methode or 'Keine ausgewählt'}"
