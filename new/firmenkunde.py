from kunde import Kunde
from validator import Validator

class Firmenkunde(Kunde):
    def __init__(self, name, adresse, email, telefon, passwort, firmennummer):
        super().__init__(name, adresse, email, telefon, passwort)


        if not Validator.validate_firmnr(firmennummer):
            raise ValueError("Ihre eingegebene Firmennummer ist ungueltig!")


        self.firmennummer = firmennummer

#Show information for Firmenkunde
    def get_info(self):
        # Basic information from the Kunde class
        basis_info = super().get_info()  
        return basis_info + f"Firmennummer: {self.firmennummer}\n"

