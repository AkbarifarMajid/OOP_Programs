from abc import ABC, abstractmethod
from utils.validator import Validator
from storage.storage import Storage

class Produkt(ABC):
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight

    @property
    def id(self):
        return self._id if hasattr(self, "_id") else None

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not Validator.validate_product_name(value):
            raise ValueError("Invalid product name.")
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not Validator.validate_price(value):
            raise ValueError("Invalid product price.")
        self._price = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not Validator.validate_weight(value):
            raise ValueError("Invalid weight.")
        self._weight = value


    '''
    def add_review(self, rating):
        if 1 <= rating <= 5:
            query = "INSERT INTO bewertungen (produkt_id, rating) VALUES (%s, %s)"
            Storage.execute_query(query, (self.id, rating))
        else:
            raise ValueError("Rating must be between 1 and 5")
    '''
    '''
    def add_review(self, rating, user_email):
        if 1 <= rating <= 5:
            existing = Storage.fetch_one(
                "SELECT id FROM bewertungen WHERE produkt_id = %s AND user_email = %s",
                (self.id, user_email)
            )

            if existing:
                # Update existing review
                query = "UPDATE bewertungen SET rating = %s WHERE id = %s"
                Storage.execute_query(query, (rating, existing[0]))
            else:
                # Add new review
                query = "INSERT INTO bewertungen (produkt_id, rating, user_email) VALUES (%s, %s, %s)"
                Storage.execute_query(query, (self.id, rating, user_email))
        else:
            raise ValueError("Rating must be between 1 and 5")
    '''

    @staticmethod
    def add_review(produkt_id, rating, user_email):
        """Add or update a review for a given product ID and user"""
        if 1 <= rating <= 5:
            # Check if the user has already rated this product
            existing = Storage.fetch_one(
                "SELECT id FROM bewertungen WHERE produkt_id = %s AND user_email = %s",
                (produkt_id, user_email)
            )
            if existing:
                # Update existing rating
                Storage.execute_query(
                    "UPDATE bewertungen SET rating = %s WHERE id = %s",
                    (rating, existing[0])
                )
            else:
                # Insert new rating
                Storage.execute_query(
                    "INSERT INTO bewertungen (produkt_id, rating, user_email) VALUES (%s, %s, %s)",
                    (produkt_id, rating, user_email)
                )
        else:
            raise ValueError("Rating must be between 1 and 5")

    @staticmethod
    def average_rating(produkt_id):
        from storage.storage import Storage
        result = Storage.fetch_one("SELECT AVG(rating) FROM bewertungen WHERE produkt_id = %s", (produkt_id,))
        return result[0] if result and result[0] is not None else 0

    #def average_rating(self, produkt_id):
    #    query = "SELECT AVG(rating) FROM bewertungen WHERE produkt_id = %s"
    #    result = Storage.fetch_one(query, (produkt_id,))
    #    return result[0] if result and result[0] is not None else 0

    @abstractmethod
    def __str__(self):
        pass
