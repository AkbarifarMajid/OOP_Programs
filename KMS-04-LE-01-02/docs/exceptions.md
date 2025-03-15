# Exception-Dokumentation (mit Standardmeldungen)

In diesem Projekt habe ich eigene Fehlermeldungen (Exceptions) mit Standardtext
erstellt, damit Fehler klar und einheitlich angezeigt werden.
---

## 1. DatenbankFehler

```
class DatenbankFehler(Exception):
    """Allgemeiner Fehler bei Datenbankoperationen."""
    def __init__(self, message="Unbekannter Datenbankfehler ist aufgetreten."):
        super().__init__(f" DatenbankFehler: {message}")
```

## 2. VerbindungsFehler

```
class VerbindungsFehler(DatenbankFehler):
    """Fehler beim Aufbau der Datenbankverbindung."""
    def __init__(self, message="Verbindung zur Datenbank fehlgeschlagen."):
        super().__init__(f" VerbindungsFehler: {message}")
```


## 3. SpeicherFehler

```
class SpeicherFehler(DatenbankFehler):
    """Fehler beim Speichern oder Laden von Daten."""
    def __init__(self, message="Fehler beim Speichern oder Laden von Daten."):
        super().__init__(f" SpeicherFehler: {message}")
```


## 4. NichtGefundenFehler

```
class NichtGefundenFehler(DatenbankFehler):
    """Fehler wenn Datensatz nicht gefunden wurde."""
    def __init__(self, message="Der angeforderte Datensatz wurde nicht gefunden."):
        super().__init__(f" NichtGefundenFehler: {message}")
```


## Verwendung im Code

     Methode                                Exception-Typ   
-----------------------------------|-----------------------------
     connect()                     |       VerbindungsFehler()
     save_customer()               |       SpeicherFehler()
     save_product()                |       SpeicherFehler() 
     load_product_with_rating()    |       NichtGefundenFehler()
     Andere DB-Operationen         |       DatenbankFehler()


## UML-Diagramm

Das folgende Diagramm zeigt die Struktur der Klassen im Projekt:

![UML](docs/uml_warenwelt.jpg)

Die editierbare Version befindet sich in: `docs/uml_warenwelt.drawio`


Datei erstellt am: 15.03.2025  
Erstellt von: Akbarifar Projekt
