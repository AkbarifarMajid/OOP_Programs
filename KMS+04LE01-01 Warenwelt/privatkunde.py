from kunde import Kunde
from validator import Validator
from datetime import datetime

class Privatkunde(Kunde):
    def __init__(self, name, adresse, email, telefon, passwort, geburtsdatum):
        super().__init__(name, adresse, email, telefon, passwort)

        if not Validator.validate_dob(geburtsdatum):
            raise ValueError("Ihr eingegebenes Geburtsdatum ist ungueltig!")

        self.geburtsdatum = geburtsdatum

    def berechne_alter(self):
        geburt = datetime.strptime(self.geburtsdatum, "%d.%m.%Y")
        heute = datetime.today()
        alter = heute.year - geburt.year

        if (heute.month, heute.day) < (geburt.month, geburt.day):
            alter -= 1

        return alter
