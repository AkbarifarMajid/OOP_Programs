

from kunden.kunde import Kunde
from kunden.privatkunde import Privatkunde
from kunden.firmenkunde import Firmenkunde

from produkte.elektronik import Elektronik
from produkte.kleidung import Kleidung
from produkte.buch import Buch

from storage.storage import Storage


from produkte.buch import Buch
from produkte.elektronik import Elektronik
from produkte.kleidung import Kleidung

from storage.exceptions import (
    DatenbankFehler,
    VerbindungsFehler,
    SpeicherFehler,
    NichtGefundenFehler
)


from storage.storage import Storage
from storage.exceptions import VerbindungsFehler

try:
    db = Storage()
    db.connect()
    db.create_tables()
    db.close()
except VerbindungsFehler as ve:
    print(" Verbindung fehlgeschlagen:", ve)
'''
# ------------------- Validate Test ----------------------------------
print(Validator.validate_email("test@example.com"))            # True
print(Validator.validate_phone("+491234567890"))               # True
print(Validator.validate_name("Ali Reza"))                     # True
print(Validator.validate_address("Straße 10, Berlin "))         # True
print(Validator.validate_birthdate("2000-01-01"))              # True
print(Validator.validate_company_number("123456789"))          # True
#-------------------------------------------------------------------------------------------
'''


'''
#--------------------------- Kunde Test -----------------------------------------
kunde1 = Kunde.create_customer("Ali", "Berlin", "ali@test.de", "+49123456789", "pass123")
print(kunde1.email)

# تست setter با مقدار اشتباه
try:
    kunde1.phone = "abc"  # نامعتبر
except ValueError as e:
    print("Fehler:", e)

# تست setter با مقدار درست
kunde1.phone = "+4987654321"
print("Neues Telefon:", kunde1.phone)

# تغییر فقط ایمیل و آدرس
kunde1.update_info(email="ali.new@mail.com", address="Berlin, Germany")

# بررسی
print(kunde1.email)
print(kunde1.address)

Kunde.show_all_customers()
#----------------------------------------------------------------------------------
'''

'''
# -------------------- Private Kunde Test -------------------------------------
kunde2 = Privatkunde(
    name="Sara",
    address="Berlin",
    email="sara1215@gmail.com",
    phone="+49123456789",
    password="AAAdd11",
    birthdate="2000-03-20"
)

print(kunde2)
#--------------------------------------------------------------------------
'''


'''
#----------------------------- Firmenkunde Test -------------------------------
kunde3 = Firmenkunde(
    name="Muster GmbH",
    address="Hamburg",
    email="info@muster.de",
    phone="+4940123456",
    password="firma123",
    company_number="1234567890"
)

print(kunde3)
#--------------------------------------------------------------------------
'''


'''
#-------------------------- Test Elektronik , Kleidung, Buch ---------------------------------
e = Elektronik("Laptop", 1200, 2.5, "Lenovo", 2)
k = Kleidung("T-Shirt", 20, 0.3, "M", "Blau")
b = Buch("1984", 15, 0.4, "George Orwell", 328)

e.add_review(5)
e.add_review(4)
k.add_review(3)
b.add_review(5)
b.add_review(4)
b.add_review(5)

print(e)
print("\n" + "-"*40 + "\n")
print(k)
print("\n" + "-"*40 + "\n")
print(b)
#-----------------------------------------------------------------------------------------
'''



# اتصال به پایگاه‌داده
#db = Storage()
#db.connect()
#db.create_tables()
#db.close()


'''
# -------------------------  add new customer -------------------------------

p1 = Privatkunde("Majid Akbarifar", "Graz", "majidakbarifar2@gmail.com", "+49123456789", "1234", "1986-07-11")
f1 = Firmenkunde("Tech GmbH", "Hamburg", "info@tech.de", "+4940123456", "abc123", "987654321")

# ذخیره در دیتابیس
#db.save_customer(p1)
#db.save_customer(f1)

'''



''''
#---------------------- Print all customers-----------------------------

kunden = db.load_all_customers()

for k in kunden:
    print("-----------------------")
    print(k)
'''



'''
#------------------ Insert Produkt-----------------------------
b = Buch("1984", 15.0, 0.4, "George Orwell", 328)
e = Elektronik("Laptop", 1200, 2.5, "Lenovo", 2)
k = Kleidung("T-Shirt", 20, 0.3, "M", "Blau")

# ذخیره در دیتابیس
db.save_product(b)
db.save_product(e)
db.save_product(k)
'''


'''
#----------- Show all Produkte--------------------------
produkte = db.load_all_products()

for p in produkte:
    print("---------------------------")
    print(p)
'''


'''
# ------------------ add Review -------------
db.add_review_to_product(1, 5)
db.add_review_to_product(1, 4)
'''


'''
#--------------- Show avg review ----------------
avg = db.get_average_rating(1)
print("📊 Durchschnittsbewertung:", round(avg, 2))
'''


'''
#------------- Show Produkte with ava review ----------------------
produkt = db.load_product_with_rating(1)
if produkt:
    print(produkt)
    print("📊 Durchschnittsbewertung:", round(produkt.average_rating(), 2))
'''


'''
# --------------- show all Produkte with avg reviews ------------------
produkte = db.load_all_products_with_rating()

for p in produkte:
    print("----------------------------")
    print(p)
    print("📊 Durchschnittsbewertung:", round(p.average_rating(), 2))
'''


'''
try:
    db.connect()
except VerbindungsFehler as ve:
    print("⚠️ Verbindungsproblem:", ve)
'''

#db.close()



