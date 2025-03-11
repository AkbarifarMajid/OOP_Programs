class Produkt:
    def __init__ (self, id, name, preis, beschreibung):
        self.id = id
        self.name = name
        self.preis = preis
        self.beschreibung = beschreibung

    def get_info(self):
        return f"{self.id}: {self.name} ({self.preis} €) - {self.beschreibung}"

    def update_preis(self, neuer_preis):
        self.preis = neuer_preis
        print(f"Der Preis von {self.name} wurde auf {self.preis} € geaendert.")

    def apply_discount(self,discount):
        self.preis = self.preis- (self.preis * discount/100)
        print(f"Der Preis von {self.name} wurde um {discount} € reduziert. Neuer Preis: {self.preis} €")