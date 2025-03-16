# WarenWelt – Online Shop System 
Dieses Projekt ist ein objektorientiertes Python-System zur Verwaltung von Kunden, Produkten und Bewertungen in einem Online-Shop.  
Es basiert auf MySQL-Datenbankintegration.

---

## Projektstruktur

`kunden/`: Kunde, Privatkunde, Firmenkunde
`produkte/`: Produkt, Buch, Elektronik, Kleidung
`storage/`: Datenbankverbindung, CRUD-Methoden
`utils/validator.py`: Validierung von Eingabefeldern
`storage/exceptions.py`: Eigene Exception-Klassen
`docs/`: UML-Diagramme, Dokumentation
`tests/test_all.py`: Kompletttest für das System

---

## Objektorientierte Konzepte

Vererbung:
  `Privatkunde` und `Firmenkunde` erben von der gemeinsamen Basisklasse `Kunde`.
  `Buch`, `Elektronik` und `Kleidung` erben von der abstrakten Klasse `Produkt`.

Abstraktion:
`Produkt` ist eine abstrakte Klasse. Es wird nie direkt instanziiert, sondern dient als Vorlage für Produkttypen.
`Kunde` kann ebenfalls als abstract betrachtet werden.

Kapselung:
  Attribute wie Name, Adresse, Preis usw. werden durch Getter/Setter geschützt und mit `Validator` validiert.

Fehlerbehandlung:
Es gibt eigene Exception-Klassen wie `SpeicherFehler`, `VerbindungsFehler`, `NichtGefundenFehler` usw.

---

## Datenbankstruktur (MySQL)

`kunden`, `privatkunden`, `firmenkunden`
`produkte`, `produkte_buch`, `produkte_elektronik`, `produkte_kleidung`
`bewertungen` zur Speicherung von Produktbewertungen

---

##  Getestete Funktionen (in `test_all.py`)

Kunden: speichern, laden, löschen
Produkte: speichern, laden, löschen
Bewertungen: hinzufügen, anzeigen, Durchschnitt berechnen
Ausnahmebehandlung in allen Datenbankoperationen
Verbindungstest und Tabellenaufbau

---

##  UML-Diagramm

Das vollständige Klassendiagramm befindet sich unter:  
`docs/uml_warenwelt.ipg`

Die bearbeitbare Version findest du unter: `docs/uml_warenwelt.drawio`

---

##  Ziel

Dieses Projekt zeigt mein Verständnis von objektorientierter Programmierung in Python mit echter Datenbankanbindung.  
Ich habe Wert auf saubere Struktur, Wiederverwendbarkeit, Fehlerbehandlung und Datenvalidierung gelegt.

 Erstellt von: Majid Akbarifar 