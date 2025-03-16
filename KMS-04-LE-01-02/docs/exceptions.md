# Exception-Dokumentation (mit Standardmeldungen)

In diesem Projekt habe ich eigene Fehlermeldungen (Exceptions) mit Standardtext
erstellt, damit Fehler klar und einheitlich angezeigt werden.
---

## 1. `DatenbankFehler` – Basisklasse für alle Datenbankfehler

```
class DatenbankFehler(Exception):
    """Allgemeiner Fehler bei Datenbankoperationen."""
    def __init__(self, message="Unbekannter Datenbankfehler ist aufgetreten."):
        super().__init__(f" DatenbankFehler: {message}")
```
Diese Klasse dient als Basis für alle anderen spezifischen Fehler.


## 2. `VerbindungsFehler` – Fehler beim Aufbau der Verbindung

```
class VerbindungsFehler(DatenbankFehler):
    """Fehler beim Aufbau der Datenbankverbindung."""
    def __init__(self, message="Verbindung zur Datenbank fehlgeschlagen."):
        super().__init__(f" VerbindungsFehler: {message}")
```
Wird ausgelöst, wenn keine Verbindung zur Datenbank aufgebaut werden kann.

## 3. `SpeicherFehler` – Fehler beim Speichern oder Laden von Daten

```
class SpeicherFehler(DatenbankFehler):
    """Fehler beim Speichern oder Laden von Daten."""
    def __init__(self, message="Fehler beim Speichern oder Laden von Daten."):
        super().__init__(f" SpeicherFehler: {message}")
```
Tritt auf, wenn Probleme beim Speichern, Aktualisieren oder Laden von Daten auftreten.

##  4. `NichtGefundenFehler` – Datensatz nicht gefunden

```
class NichtGefundenFehler(DatenbankFehler):
    """Fehler wenn Datensatz nicht gefunden wurde."""
    def __init__(self, message="Der angeforderte Datensatz wurde nicht gefunden."):
        super().__init__(f" NichtGefundenFehler: {message}")
```
Wird verwendet, wenn ein Datensatz (z.B. Produkt oder Kunde) nicht in der Datenbank existiert.

## Verwendung im Code

 Methode                        Exception-Typ           

 `connect()`                   `VerbindungsFehler()`   
 `create_tables()`             `SpeicherFehler()`      
 `save_customer()`             `SpeicherFehler()`      
 `load_all_customers()`        `DatenbankFehler()`     
 `save_product()`              `SpeicherFehler()`      
 `load_all_products()`         `DatenbankFehler()`     
 `add_review_to_product()`     `SpeicherFehler()`      
 `load_product_with_rating()`  `NichtGefundenFehler()` 
 `delete_customer()`           `SpeicherFehler()`      
 `delete_product()`            `SpeicherFehler()`      


##  Vorteile dieser Struktur

Einheitliche Fehlerbehandlung im gesamten Projekt  
Aussagekräftige und verständliche Fehlermeldungen  
Klare Trennung der Fehlerarten  
Bessere Testbarkeit und Wartbarkeit


Erstellt von: Majid Akbarifar 
