#  Base class
from kunden.kunde import Kunde

#  Validator
from utils.validator import Validator


class Firmenkunde(Kunde):
    def __init__(self, name, address, email, phone, password, company_number):
        super().__init__(name, address, email, phone, password)
        self.company_number = company_number  # setter handles validation

    @property
    def company_number(self):
        return self._company_number

    @company_number.setter
    def company_number(self, value):
        if not Validator.validate_company_number(value):
            raise ValueError("Invalid company number.")
        self._company_number = value

    def __str__(self):
        base_info = (
            f"Name: {self.name}\n"
            f"Adresse: {self.address}\n"
            f"E-Mail: {self.email}\n"
            f"Telefon: {self.phone}\n"
            f"Passwort: {self.password}"
        )
        return f"{base_info}\nCompany: {self.company_number}"

