
import mysql.connector
from mysql.connector import Error
from storage.exceptions import (
    VerbindungsFehler,
    SpeicherFehler,
    DatenbankFehler
)

class Storage:
    _conn = None
    _cursor = None

    @classmethod
    def connect(cls):
        if not cls._conn:
            try:
                cls._conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Akbarifar6503",
                    database="online_shop_warenwelt_2"
                )
                cls._cursor = cls._conn.cursor(buffered=True)
                print("-- connect --")
            except mysql.connector.Error:
                raise VerbindungsFehler()

    @classmethod
    def disconnect(cls):
        if cls._conn:
            cls._cursor.close()
            cls._conn.close()
            cls._conn = None
            cls._cursor = None
            print("--  Disconnect --")

    @classmethod
    def execute_query(cls, query, params=None):
        try:
            cls.connect()
            cls._cursor.execute(query, params)
            cls._conn.commit()
        except mysql.connector.Error:
            raise SpeicherFehler()

    @classmethod
    def fetch_one(cls, query, params=None):
        try:
            cls.connect()
            cls._cursor.execute(query, params)
            return cls._cursor.fetchone()
        except mysql.connector.Error:
            raise DatenbankFehler()

    @classmethod
    def fetch_all(cls, query, params=None):
        try:
            cls.connect()
            cls._cursor.execute(query, params)
            return cls._cursor.fetchall()
        except mysql.connector.Error:
            raise DatenbankFehler()

    @classmethod
    def insert_and_get_id(cls, query, params=None):
        try:
            cls.connect()
            cls._cursor.execute(query, params)
            cls._conn.commit()
            return cls._cursor.lastrowid
        except mysql.connector.Error:
            raise SpeicherFehler()