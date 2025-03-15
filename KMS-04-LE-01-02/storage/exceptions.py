# exceptions.py

class DatenbankFehler(Exception):
    """Allgemeiner Fehler bei Datenbankoperationen."""
    def __init__(self, message="Unbekannter Datenbankfehler ist aufgetreten."):
        super().__init__(f"❗ DatenbankFehler: {message}")


class VerbindungsFehler(DatenbankFehler):
    """Fehler beim Aufbau der Datenbankverbindung."""
    def __init__(self, message="Verbindung zur Datenbank fehlgeschlagen."):
        super().__init__(f"🔌 VerbindungsFehler: {message}")


class SpeicherFehler(DatenbankFehler):
    """Fehler beim Speichern oder Laden von Daten."""
    def __init__(self, message="Fehler beim Speichern oder Laden von Daten."):
        super().__init__(f"💾 SpeicherFehler: {message}")


class NichtGefundenFehler(DatenbankFehler):
    """Fehler wenn Datensatz nicht gefunden wurde."""
    def __init__(self, message="Der angeforderte Datensatz wurde nicht gefunden."):
        super().__init__(f"🔍 NichtGefundenFehler: {message}")
