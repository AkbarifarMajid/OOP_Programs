# This class handles payment (Zahlung) information and saves it in the database

from datetime import datetime
from storage.storage import Storage

class Zahlung:
    def __init__(self, method):
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

    # Create a payment entry in the database
    def erstelle_zahllung(self):
        self._id = Storage.insert_and_get_id(
            """
            INSERT INTO zahllung (zahllung_method, zahllung_datum)
            VALUES (%s, %s)
            """,
            (self.method, self.datum)
        )

    # Return all available payment methods
    def get_alle_methoden(self):
        return self.methoden

    # Choose a payment method from the list using index
    def methode_waehlen(self, auswahl_index: int):
        if 1 <= auswahl_index <= len(self.methoden):
            # Set the selected method (adjusted for list index starting at 0)
            self.gewaehlte_methode = self.methoden[auswahl_index - 1]
            return self.gewaehlte_methode
        else:
            raise ValueError("Ungültige Auswahl für Zahlungsmethode.")

    # Return a string representation of the selected method
    def __str__(self):
        return f"Zahlungsmethode: {self.gewaehlte_methode or 'Keine ausgewählt'}"
