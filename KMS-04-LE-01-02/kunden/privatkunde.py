#  Standard Libraries
from datetime import datetime

#  Base class
from kunden.kunde import Kunde

#  Validator
from utils.validator import Validator

class Privatkunde(Kunde):
    def __init__(self, name, address, email, phone, password, birthdate):
        super().__init__(name, address, email, phone, password)
        self.birthdate = birthdate  # setter handles validation

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value):
        if not Validator.validate_birthdate(value):
            raise ValueError("Ungültiges Geburtsdatum.")
        self._birthdate = value

    def calculate_age(self):
        birth = datetime.strptime(self.birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth.year
        if (today.month, today.day) < (birth.month, birth.day):
            age -= 1
        return age

    def __str__(self):
        base_info = (
            f"Name: {self.name}\n"
            f"Adresse: {self.address}\n"
            f"E-Mail: {self.email}\n"
            f"Telefon: {self.phone}\n"
            f"Passwort: {self.password}"
        )
        return f"{base_info}\nGeburtsdatum: {self.birthdate}\nAlter: {self.calculate_age()} Jahre"
