class Zahlung:
    def __init__(self, id, bestellung, betrag):
        self.id = id
        self.bestellung = bestellung
        self.betrag = betrag
        self.status = "In Bearbeitung"

    def payment_status(self):
        return f"Zahlungsstatus für Bestellung {self.bestellung.id}: {self.status}"

    def update_payment_status(self, neuer_status):
        self.status = neuer_status
        print(f"Zahlungsstatus für Bestellung {self.bestellung.id} wurde auf {self.status} aktualisiert.")
