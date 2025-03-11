from itertools import product


class Bestellung:
    def __init__(self, id, kunde):
        self.id = id
        self.kunde = kunde
        self.produkte = []
        self.bestell_datum = "2025-03-11"

    def add_produkt(self, produkt):
        self.produkte.append(produkt)
        print(f"{produkt.name} wurde zur Bestellung hinzugefügt.")

    def get_bestellung_info(self):
        produkte_info  = [f"{produkt.name} {produkt.preis} € " for produkt in self.produkte]
        return f"Bestellung {self.id} von {self.kunde.name} ({self.kunde.email}) : {', '.join(produkte_info)}"


    def calculate_total(self):
        total = sum(product.preis for product in self.produkte)
        if self.kunde.vip_status== True:
            total = total * 0.9
            print("VIP Rabatt angewendet.")

        return f"Total: {total} €"