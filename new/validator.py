# -*- coding: utf-8 -*-

import re
from datetime import datetime

"""
This class contains static methods for validating input.
"""

class Validator:

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
        return re.match(pattern, email) is not None


    @staticmethod
    def validate_phone(phone: str) -> bool:
     if phone.startswith("+"):
        phone = phone[1:]
     return phone.isdigit() and 8 <= len(phone) <= 20


    @staticmethod
    def validate_name(name: str) -> bool:
        pattern = r"^[A-Za-zÄÖÜäöüß\s\-']{2,}$"
        return re.match(pattern, name) is not None


    @staticmethod
    def validate_address(address: str) -> bool:
        pattern = r"^[A-Za-z0-9ÄÖÜäöüß\s,\.\-\/]{5,}$"
        return re.match(pattern, address) is not None


    @staticmethod
    def validate_dob(dob: str) -> bool:
        try:
            datetime.strptime(dob, "%d.%m.%Y")
            return True
        except ValueError:
            return False


    @staticmethod
    def validate_firmnr(firmnr: str) -> bool:
        return firmnr.isdigit() and 5 <= len(firmnr) <= 15

