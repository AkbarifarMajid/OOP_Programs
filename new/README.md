#  Projekt: WarenWelt – Objektorientierte Programmierung mit Python

##  Projektbeschreibung
Dieses Projekt wurde im Rahmen des Moduls „Objektorientierte Programmierung“ entwickelt und zeigt die Verwaltung von Kund*innen in einem Online-Shop-System. Die Implementierung erfolgte mit der Programmiersprache Python.

##  Klassenstruktur

### `Kunde` (Basisklasse)
- Attribute: `id`, `name`, `adresse`, `email`, `telefon`, `passwort`
- Methoden: `create()`, `update()`, `delete()`, `get_info()`, `get_all()`
- Validierung durch Klasse `Validator`

### `Privatkunde` (abgeleitete Klasse)
- Zusätzliche Attribut: `geburtsdatum`
- Methode: `berechne_alter()`

### Firmenkunde (abgeleitete Klasse)
- Zusätzliche Attribut: firmennummer
- Überschreibt get_info(), um Firmennummer anzuzeigen

##  Test & Benutzeroberfläche

### main.py
Eine einfache textbasierte Benutzeroberfläche mit folgenden Optionen:
1. Privatkunde erstellen  
2. Firmenkunde erstellen  
3. Alle Kunden anzeigen  
4. Kunde aktualisieren  
5. Kunde löschen  
0. Beenden

##  Projektstruktur
OOP_Programs/
├── KMS_04_LE_01_01_WarenWelt/
│   ├── kunde.py
│   ├── privatkunde.py
│   ├── firmenkunde.py
│   ├── validator.py
│   ├── main.py
│   ├── test_classes.py
│   ├── UML.drawio
│   ├── UML.png
│   └── README.md


## UML-Diagramm
Das Klassendiagramm befindet Sie in der Datei `KMS+04-LE-01-01-Onlineshop.drawio` (editierbar) sowie als Bild `KMS+04-LE-01-01-Onlineshop.png`.

## Projekt ausführen
```bash
python main.py