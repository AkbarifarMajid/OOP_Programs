
class DatenbankFehler(Exception):
    def __init__(self, message="Unbekannter Datenbankfehler ist aufgetreten."):
        super().__init__(message)

class VerbindungsFehler(DatenbankFehler):
    def __init__(self, message="Verbindung zur Datenbank fehlgeschlagen."):
        super().__init__(message)

class SpeicherFehler(DatenbankFehler):
    def __init__(self, message="Fehler beim Speichern oder Laden von Daten."):
        super().__init__(message)

class NichtGefundenFehler(DatenbankFehler):
    def __init__(self, message="Der angeforderte Datensatz wurde nicht gefunden."):
        super().__init__(message)
