from warenkorb.warenkorb import Warenkorb
from kunden.privatkunde import Privatkunde
from produkte.buch import Buch
from produkte.elektronik import Elektronik


buch = Buch.get_book_by_id(1)
elek = Elektronik.get_electronic_by_id(4)

kunde = Privatkunde.get_privat_by_id(1)

print(buch)
print(elek)
print(kunde)
#wk = Warenkorb(kunde)


#wk.produkt_hinzufuegen(buch)
#wk.produkt_hinzufuegen(elek)


#rint("\n Inhalt des Warenkorbs:")
#print(wk)
