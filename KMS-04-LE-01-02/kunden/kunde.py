

from abc import ABC, abstractmethod
from utils.validator import Validator

class Kunde(ABC):
    """
    Abstrakte Basisklasse für alle Kundentypen.
    Enthält gemeinsame Attribute und Validierung über Setter.
    """

    def __init__(self, name, address, email, phone, password):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.password = password

    # ----------------------------
    # Read-only ID property
    @property
    def id(self):
        return self._id if hasattr(self, "_id") else None

    # ----------------------------
    # Name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not Validator.validate_name(value):
            raise ValueError("Invalid name")
        self._name = value

    # ----------------------------
    # Adresse
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not Validator.validate_address(value):
            raise ValueError("Invalid address")
        self._address = value

    # ----------------------------
    # E-Mail
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not Validator.validate_email(value):
            raise ValueError("Invalid email address")
        self._email = value

    # ----------------------------
    # Telefon
    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if not Validator.validate_phone(value):
            raise ValueError("Invalid phone number")
        self._phone = value

    # ----------------------------
    # Passwort
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not value:
            raise ValueError("Password must not be empty")
        self._password = value

    # ----------------------------
    # Abstrakte Methode für Darstellung
    @abstractmethod
    def __str__(self):
        pass
