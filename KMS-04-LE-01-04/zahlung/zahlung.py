# zahlung/zahlung.py

class Zahlung:
    def __init__(self):
        # لیست روش‌های پرداخت ممکن
        self.methoden = ["Kreditkarte", "PayPal", "Rechnung"]
        self.gewaehlte_methode = None

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
