import re
from datetime import datetime


class Validator:

    # -------- Kunden --------


    @staticmethod
    def validate_name(name):

        pattern = r"^[A-Za-zÄÖÜäöüß\s\.'\-]+$"
        return isinstance(name, str) and re.match(pattern, name) is not None

    @staticmethod
    def validate_address(address):
        return isinstance(address, str) and len(address.strip()) > 5

    @staticmethod
    def validate_email(email):
        return isinstance(email, str) and "@" in email and "." in email

    @staticmethod
    def validate_phone(phone):

        return isinstance(phone, str) and re.fullmatch(r"^\+?\d{7,15}$", phone)


    @staticmethod
    def validate_birthdate(birthdate):
        if not isinstance(birthdate, str):
            return False
        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_company_number(company_number):
        return isinstance(company_number, str) and company_number.isdigit() and 5 <= len(company_number) <= 15

    @staticmethod
    def validate_password(password):
        return isinstance(password, str) and len(password) >= 4

        # -------- Produkte --------

    @staticmethod
    def validate_product_name(name):
        return isinstance(name, str) and len(name.strip()) >= 2

    @staticmethod
    def validate_price(price):
        return isinstance(price, (int, float)) and price >= 0

    @staticmethod
    def validate_weight(weight):
        return isinstance(weight, (int, float)) and weight >= 0

    @staticmethod
    def validate_author(author):
        return isinstance(author, str) and len(author.strip()) >= 2

    @staticmethod
    def validate_pages_count(pages_count):
        return isinstance(pages_count, int) and pages_count > 0

    @staticmethod
    def validate_brand(brand):
        return isinstance(brand, str) and len(brand.strip()) >= 2

    @staticmethod
    def validate_warranty_years(years):
        return isinstance(years, int) and years >= 0

    @staticmethod
    def validate_size(size):
        return isinstance(size, str) and len(size.strip()) >= 1

    @staticmethod
    def validate_color(color):
        return isinstance(color, str) and len(color.strip()) >= 2
    @staticmethod
    def validate_register(name, adresse, email, telefon, passwort, geburtsdatum):
        return (
            Validator.validate_name(name) and
            Validator.validate_address(adresse) and
            Validator.validate_email(email) and
            Validator.validate_phone(telefon) and
            Validator.validate_password(passwort) and
            Validator.validate_birthdate(geburtsdatum)
        )
