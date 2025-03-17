# WarenWelt – Online Shop System

Dieses Projekt ist ein objektorientiertes Python-System zur Verwaltung von Kunden, Produkten und Bewertungen in einem Online-Shop.  
Es verwendet eine MySQL-Datenbank zur persistenten Speicherung.

---

# Projektstruktur

- `kunden/`: Kunde, Privatkunde, Firmenkunde  
- `produkte/`: Produkt (abstrakt), Buch, Elektronik, Kleidung  
- `storage/`: Klasse `Storage` für Datenbankverbindung & CRUD-Operationen  
- `utils/validator.py`: Eingabevalidierung über statische Methoden  
- `storage/exceptions.py`: Eigene Fehlerklassen für strukturierte Fehlerbehandlung  
- `docs/`: UML-Diagramm, Exceptions-Doku  
- `tests/test_all.py`: Kompletttest aller Funktionen

---

# Objektorientierte Konzepte

Vererbung:  
- `Privatkunde` und `Firmenkunde` erben von `Kunde`  
- `Buch`, `Elektronik` und `Kleidung` erben von der abstrakten Klasse `Produkt`

Abstraktion: 
- `Produkt` ist abstrakt (mit `@abstractmethod`) und kann nicht direkt instanziiert werden.  
- `Kunde` ist ebenfalls eine Basisklasse und wird nie direkt erstellt.

Kapselung:  
- Attribute wie Name, Preis, Gewicht, Adresse usw. werden durch Property-Methoden geschützt.  
- Die Validierung erfolgt zentral über die Klasse `Validator`.

Fehlerbehandlung:  
- Eigene Fehlerklassen wie `SpeicherFehler`, `VerbindungsFehler`, `NichtGefundenFehler` usw.  
- Einheitliche Fehlerstruktur und bessere Testbarkeit.

---

# Datenbankstruktur (MySQL)

- Kunden:
  - `kunden`, `privatkunden`, `firmenkunden`

- Produkte:
  - `produkte`, `produkte_buch`, `produkte_elektronik`, `produkte_kleidung`

- Bewertungen:
  - `bewertungen`: Speicherung von Produktbewertungen (1–5 Sterne)

---

# Implementierte Funktionen

### Kunden
- `save_customer(kunde)`  
- `load_customer_by_id(db_kunde_id)`  
- `update_customer(kunde)`  
- `delete_customer(db_kunde_id)`  
- `load_all_customers()`

###  Produkte
- `save_product(produkt)`  
- `load_product_with_rating(db_produkt_id)`  
- `load_all_products()`  
- `load_all_products_with_rating()`  
- `delete_product(db_produkt_id)`

### Bewertungen
- `add_review_to_product(db_produkt_id, rating)`  
- `get_average_rating(db_produkt_id)`

---

##  Tests

Im Testskript `test_all.py` werden alle Funktionen vollständig getestet:

- Kundenerstellung, -bearbeitung, -löschung
- Produktspeicherung, Laden mit und ohne Bewertung
- Bewertungen und Durchschnittsberechnung
- Fehlerbehandlung bei Verbindungsfehlern oder SQL-Problemen

---

##  UML-Diagramm

Das vollständige UML-Diagramm befindet sich unter:

 `docs/uml_warenwelt.jpg`  
 Bearbeitbare Version: `docs/uml_warenwelt.drawio`

---

##  Ziel

Ziel des Projekts ist es zu zeigen, dass ich objektorientierte Programmierung mit Python verstehe,  
sowie Datenbanken, Vererbung, Fehlerbehandlung und sauberen Code in einem echten Anwendungsszenario umsetzen kann.

---

 Erstellt von: Majid Akbarifar
