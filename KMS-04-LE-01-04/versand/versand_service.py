# This class handles shipping options and calculates shipping costs

class VersandService:
    def __init__(self, produkte):
        self.lieferoptionen = [
            "Standardversand",
            "Expressversand",
            "Same-Day-Delivery",
            "Abholung im Laden"
        ]
        self.produkte = produkte
        self.gesamtgewicht = self.berechne_gesamtgewicht()
        self.versandkosten = 0.0
    '''
    # Let the user choose a delivery option
    def lieferung_auswahl(self):
        print("\nVerfügbare Lieferoptionen:")
        for i, option in enumerate(self.lieferoptionen, 1):
            print(f"{i}. {option}")
        try:
            auswahl = int(input("\nBitte wählen Sie eine Lieferoption (1-4): "))
            if 1 <= auswahl <= len(self.lieferoptionen):
                return self.lieferoptionen[auswahl - 1]
            else:
                raise ValueError("Ungültige Auswahl")
        except ValueError:
            raise ValueError("Bitte eine gültige Zahl eingeben!")
    '''
    # Calculate total weight of all products
    def berechne_gesamtgewicht(self):
        # Gesamtgewicht aus allen Produkten berechnen
        return sum(getattr(p, 'weight', 0) for p in self.produkte)

    # Calculate shipping cost based on chosen delivery method
    def berechne_versandkosten(self, methode):
        # Versandkosten nach Methode berechnen
        kosten_faktoren = {
            "Standardversand": 1.0,
            "Expressversand": 2.0,
            "Same-Day-Delivery": 3.0,
            "Abholung im Laden": 0.0
        }

        if methode not in kosten_faktoren:
            raise ValueError("Unbekannte Liefermethode")

        if methode == "Abholung im Laden":
            self.versandkosten = 0.0
        else:
            basis = 5.0
            faktor = kosten_faktoren[methode]
            self.versandkosten = basis + self.gesamtgewicht * faktor

        return round(self.versandkosten, 2)

