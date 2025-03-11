# -*- coding: utf-8 -*-

from validator import Validator
kunden_list = []

class Kunde:
    _id_kunde = 1

    def __init__(self, name, adresse, email, telefon, passwort):

        self.id = Kunde._id_kunde
        Kunde._id_kunde += 1

        self.name = name
        self.adresse = adresse
        self.email = email
        self.telefon = telefon
        self.passwort = passwort

# Getter und Setter für name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not Validator.validate_name(value):
            raise ValueError("Ihr eingegebener Name ist ungültig!")
        self._name = value

# Getter und Setter für adresse
    @property
    def adresse(self):
        return self._adresse

    @adresse.setter
    def adresse(self, value):
        if not Validator.validate_address(value):
            raise ValueError("Ihre eingegebene Adresse ist ungueltig!")
        self._adresse = value

# Getter und Setter für email
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not Validator.validate_email(value):
            raise ValueError("Ihre eingegebene E-Mail ist ungueltig!")
        self._email = value

# Getter und Setter für telefon
    @property
    def telefon(self):
        return self._telefon

    @telefon.setter
    def telefon(self, value):
        if not Validator.validate_phone(value):
            raise ValueError("Ihre eingegebene Telefonnummer ist ungueltig!")
        self._telefon = value

# Information display function
    def get_info(self):
            return (
                f"Kundennummer: {self.id}\n"
                f"Name: {self.name}\n"
                f"Adresse: {self.adresse}\n"
                f"E-Mail: {self.email}\n"
                f"Telefon: {self.telefon}\n"

             )

# Add Kunde to list
    def create(self):
        kunden_list.append(self)
        print(f"Kunde {self.name} mit Id {self.id} wurde erfolgreich in die Kundenliste hinzufuegt!")

#update kunden info
    @staticmethod
    def update(id, feld, neuer_wert):
        for kunde in kunden_list:
            if kunde.id == id:
                if feld == "name":
                    kunde.name = neuer_wert
                elif feld == "adresse":
                    kunde.adresse = neuer_wert
                elif feld == "email":
                    kunde.email = neuer_wert
                elif feld == "telefon":
                    kunde.telefon = neuer_wert
                elif feld == "passwort":
                    kunde.passwort = neuer_wert
                else:
                    print("Sie haben kein gültiges Feld angegeben.")
                    return
                print(f"Feld '{feld}' für Kunde mit Id {id} wurde erfolgreich aktualisiert.")
                return
        print(f"Kein Kunde mit Id {id} gefunden.")

#delete kunden info
    @staticmethod
    def delete(id):
        for kunde in kunden_list:
            if kunde.id == id:
                kunden_list.remove(kunde)
                print(f"Kunde mit Id {id} wurde erfolgreich geloescht.")
                return
        print(f"Kein Kunde mit Id {id} gefunden.")

#show alle kunden liste
    @staticmethod
    def get_all():
        if not kunden_list:
            print("Keine Kunden gefunden.")
            return

        print("Alle Kunden in der Liste:")
        for kunde in kunden_list:
            print("-----------------------")
            print(kunde.get_info())