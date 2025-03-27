# Built-in and Flask imports
from flask import request, render_template, redirect, url_for, session
from app import app

#  Exceptions
from storage.exceptions import (
    SpeicherFehler,
    VerbindungsFehler,
    NichtGefundenFehler,
    DatenbankFehler
)

# Storage
from storage.storage import Storage

# Product Modules
from produkte.produkt import Produkt
from produkte.buch import Buch
from produkte.kleidung import Kleidung
from produkte.elektronik import Elektronik

# Customer Modules
from kunden.privatkunde import Privatkunde
from kunden.firmenkunde import Firmenkunde

# Order & Payment
from bestellung.bestellung import Bestellung
from zahlung.zahlung import Zahlung

#  Utils
from utils.validator import Validator


@app.route("/")
def startseite():
    return redirect(url_for("produkte_anzeigen"))

# user login checks the email and password and starts a session if correct.
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Checking the existence of emails in the database
            row = Storage.fetch_one("SELECT password FROM kunden WHERE email = %s", (email,))
            if not row:
                raise NichtGefundenFehler("E-Mail ist nicht registriert.")

            if row[0] != password:
                raise SpeicherFehler("Falsches Passwort.")

            # User successfully logged in
            session["user"] = email
            return redirect(url_for("produkte_anzeigen"))

        except NichtGefundenFehler as e:
            error = str(e)
        except SpeicherFehler as e:
            error = str(e)
        except Exception:
            error = "Ein unerwarteter Fehler ist aufgetreten."

    return render_template("login.html", error=error)

# Handles user registration for private and business customers with validation and session login.
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        name = request.form["name"]
        adresse = request.form["adresse"]
        email = request.form["email"]
        telefon = request.form["telefon"]
        passwort = request.form["passwort"]
        typ = request.form["typ"]
        geburtsdatum = request.form.get("geburtsdatum", "")
        firmenbuchnummer = request.form.get("firmenbuchnummer", "")

        try:
            if typ == "privat":
                if not Validator.validate_register(name, adresse, email, telefon, passwort, geburtsdatum):
                    raise SpeicherFehler("Ungültige Eingaben für Privatkunde.")

                kunde_id = Privatkunde.create_customer(name, adresse, email, telefon, passwort, geburtsdatum)
                if not kunde_id:
                    raise SpeicherFehler("E-Mail ist bereits registriert.")

            elif typ == "firma":
                if not Validator.validate_company_number(firmenbuchnummer):
                    raise SpeicherFehler("Ungültige Firmenbuchnummer.")

                kunde_id = Firmenkunde.create_customer(name, adresse, email, telefon, passwort, firmenbuchnummer)
                if not kunde_id:
                    raise SpeicherFehler("E-Mail ist bereits registriert.")

            # ✅ Erfolgreiche Registrierung – Weiterleitung
            session["user"] = email
            return redirect(url_for("produkte_anzeigen"))

        except SpeicherFehler as e:
            error = f"❌ Registrierung fehlgeschlagen: {e}"

        except Exception:
            # Allgemeiner Datenbankfehler
            error = "❌ Ein unerwarteter Fehler ist aufgetreten."

        return render_template("register.html", error=error, form_data=request.form)

    # GET-Anfrage – Zeige das Formular
    return render_template("register.html", form_data=None)

# This route logs the user out by removing them from the session
@app.route("/logout")
def logout():
    # Remove "user" from the session (log the user out)
    session.pop("user", None)

    # Redirect to the login page
    return redirect(url_for("login"))


# This route displays all products and ratings
@app.route("/produkte")
def produkte_anzeigen():
    # Check if user is logged in
    if "user" not in session:
        return redirect(url_for("login"))

    try:
        # Get user's email
        email = session.get("user")

        # Load user details from database
        row = Storage.fetch_one("SELECT name, kundentyp FROM kunden WHERE email = %s", (email,))
        name, typ = row if row else ("Unbekannt", "Gast")

        # Load all products
        buecher = Buch.get_all_books() or []
        elektro = Elektronik.get_all_electronics() or []
        kleider = Kleidung.get_all_clothing() or []

        # Get selected category and sorting
        kategorie = request.args.get("kategorie") or ""
        sortierung = request.args.get("sortierung") or ""

        produkte = []

        # Collect all products and ratings
        for liste, typ_name, extra_format in [
            (buecher, "Buch", lambda p: f"Autor: {p[4]}, Seiten: {p[5]}"),
            (elektro, "Elektronik", lambda p: f"Marke: {p[4]}, Volt: {p[5]}"),
            (kleider, "Kleidung", lambda p: f"Größe: {p[4]}, Farbe: {p[5]}")
        ]:
            for p in liste:
                produkt_id = p[0]

                # Use our own method to get rating
                avg_rating = Produkt.average_rating(produkt_id)

                # Fetch rating count
                row = Storage.fetch_one("SELECT COUNT(*) FROM bewertungen WHERE produkt_id = %s", (produkt_id,))
                anzahl_bewertungen = row[0] if row else 0

                produkte.append({
                    "id": produkt_id,
                    "name": p[1],
                    "price": p[2],
                    "typ": typ_name,
                    "extra": extra_format(p),
                    "rating": avg_rating,
                    "anzahl_bewertungen": anzahl_bewertungen
                })

        # Apply category filter
        if kategorie:
            produkte = [p for p in produkte if p["typ"] == kategorie]

        # Apply sorting
        if sortierung == "preis_auf":
            produkte.sort(key=lambda x: x["price"])
        elif sortierung == "preis_ab":
            produkte.sort(key=lambda x: x["price"], reverse=True)
        elif sortierung == "name_auf":
            produkte.sort(key=lambda x: x["name"].lower())
        elif sortierung == "name_ab":
            produkte.sort(key=lambda x: x["name"].lower(), reverse=True)

        # Remove duplicates
        unique_keys = set()
        unique_produkte = []
        for p in produkte:
            key = (p["name"], p["typ"], p["price"])
            if key not in unique_keys:
                unique_keys.add(key)
                unique_produkte.append(p)

        produkte = unique_produkte

        # Send data to frontend
        return render_template(
            "produkte.html",
            produkte=produkte,
            user_email=email,
            name=name,
            typ=typ,
            sortierung=sortierung,
            kategorie=kategorie
        )

    except Exception as e:
        raise SpeicherFehler("Produkte konnten nicht geladen werden.") from e


# Route to add a product to the shopping cart
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if "user" not in session:
        return redirect(url_for("login"))

    try:
        name = request.form["name"]
        typ = request.form["typ"]

        produkt = None

        # Try to load product based on its type and name
        if typ == "Buch":
            for b in Buch.get_all_books():
                if b[1] == name:
                    produkt = Buch(name=b[1], price=b[2], weight=b[3], author=b[4], pages_count=b[5])
                    produkt.id = b[0]
                    break

        elif typ == "Elektronik":
            for e in Elektronik.get_all_electronics():
                if e[1] == name:
                    produkt = Elektronik(name=e[1], price=e[2], weight=e[3], brand=e[4], warranty_years=e[5])
                    produkt.id = e[0]
                    break

        elif typ == "Kleidung":
            for k in Kleidung.get_all_clothing():
                if k[1] == name:
                    produkt = Kleidung(name=k[1], price=k[2], weight=k[3], size=k[4], color=k[5])
                    produkt.id = k[0]
                    break

        # Produkt not found
        if produkt is None:
            raise NichtGefundenFehler("Produkt nicht gefunden.")

        # Initialize cart in session if not available
        if "warenkorb" not in session:
            session["warenkorb"] = []

        warenkorb = session["warenkorb"]

        # Add or update product in cart
        for item in warenkorb:
            if item["id"] == produkt.id:
                item["anzahl"] += 1
                break
        else:
            warenkorb.append({
                "id": produkt.id,
                "name": produkt.name,
                "price": produkt.price,
                "typ": typ,
                "anzahl": 1
            })

        session["warenkorb"] = warenkorb

    except NichtGefundenFehler as e:
        print(e)
        return str(e)

    except Exception as e:
        print(" Fehler beim Hinzufügen zum Warenkorb:", e)
        raise SpeicherFehler("Fehler beim Hinzufügen zum Warenkorb.")

    # Redirect back with filters
    kategorie = request.form.get("kategorie", "")
    sortierung = request.form.get("sortierung", "")
    return redirect(url_for("produkte_anzeigen", kategorie=kategorie, sortierung=sortierung))


# Route to remove a product from the shopping cart
@app.route("/cart/remove/<int:id>")
def produkt_entfernen(id):
    try:
        if "warenkorb" in session:
            warenkorb = session["warenkorb"]

            # Remove product with matching ID
            warenkorb = [p for p in warenkorb if p["id"] != id]

            session["warenkorb"] = warenkorb

    except Exception as e:
        print("Fehler beim Entfernen des Produkts aus dem Warenkorb:", e)
        raise SpeicherFehler("Produkt konnte nicht entfernt werden.")

    return redirect(url_for("warenkorb_anzeigen"))


# Route to decrease the quantity of a product in the cart
@app.route("/cart/decrease/<int:id>")
def produkt_verringern(id):
    try:
        if "warenkorb" in session:
            warenkorb = session["warenkorb"]

            # Loop through items and reduce quantity
            for item in warenkorb:
                if item["id"] == id:
                    if item["anzahl"] > 1:
                        item["anzahl"] -= 1
                    else:
                        warenkorb.remove(item)
                    break

            session["warenkorb"] = warenkorb

    except Exception as e:
        print("❌ Fehler beim Verringern der Produktanzahl:", e)
        raise SpeicherFehler("Produktanzahl konnte nicht verringert werden.")

    return redirect(url_for("warenkorb_anzeigen"))


# Route to increase the quantity of a product in the shopping cart
@app.route("/cart/increase/<int:id>")
def produkt_erhoehen(id):
    try:
        if "warenkorb" in session:
            warenkorb = session["warenkorb"]

            # Find the product and increase its quantity
            for item in warenkorb:
                if item["id"] == id:
                    item["anzahl"] += 1
                    break

            session["warenkorb"] = warenkorb

    except Exception as e:
        print(" Fehler beim Erhöhen der Produktanzahl:", e)
        raise SpeicherFehler("Produktanzahl konnte nicht erhöht werden.")

    return redirect(url_for("warenkorb_anzeigen"))


# Route to completely clear the shopping cart and return to the product page
@app.route("/clear_cart")
def clear_cart():
    try:
        # Try to remove the 'warenkorb' (shopping cart) from session
        session.pop("warenkorb", None)

    except Exception as e:
        print("Fehler beim Leeren des Warenkorbs:", e)
        raise SpeicherFehler("Warenkorb konnte nicht geleert werden.")

    # Redirect to the product listing page
    return redirect(url_for("produkte_anzeigen"))


# Route to display the shopping cart
@app.route("/warenkorb")
def warenkorb_anzeigen():
    # Check if user is logged in
    if "user" not in session:
        return redirect(url_for("login"))

    try:
        # Try to get the shopping cart and user email from the session
        warenkorb = session.get("warenkorb", [])
        user_email = session.get("user", "Gast")

        # Render the cart page with cart data and user email
        return render_template("warenkorb.html", warenkorb=warenkorb, user_email=user_email)

    except Exception as e:
        print("Fehler beim Anzeigen des Warenkorbs:", e)
        raise SpeicherFehler("Warenkorb konnte nicht angezeigt werden.")


# Route to handle the submission of an order (from shopping cart)
@app.route("/bestellen", methods=["POST"])
def bestellung_absenden():
    try:
        warenkorb = session.get("warenkorb", [])

        lieferart = request.form.get("lieferart", "Standardversand")
        zahlungsmethode = request.form.get("zahlung", "Kreditkarte")

        produkte = []

        for item in warenkorb:
            typ = item["typ"]
            name = item["name"]
            price = float(item["price"])
            anzahl = item.get("anzahl", 1)

            produkt = Storage.fetch_one(
                "SELECT id FROM produkte WHERE name = %s AND price = %s",
                (name, price)
            )

            if produkt:
                class DummyProdukt:
                    def __init__(self, id_, name, price, anzahl=1):
                        self.id = id_
                        self.name = name
                        self.price = price
                        self.anzahl = anzahl

                produkte.append(DummyProdukt(produkt[0], name, price, anzahl))

        email = session.get("user")

        row = Storage.fetch_one("SELECT id, kundentyp FROM kunden WHERE email = %s", (email,))
        if not row:
            raise NichtGefundenFehler("Kunde nicht gefunden.")

        kunde_id, kundentyp = row

        if kundentyp == "firma":
            kunde = Firmenkunde.get_firma_by_id(kunde_id)
            kunde.kundentyp = "firma"
        else:
            kunde = Privatkunde.get_privat_by_id(kunde_id)
            kunde.kundentyp = "privat"

        zahlung = Zahlung(zahlungsmethode)
        zahlung.id = 1  # Dummy value

        bestellung = Bestellung(kunde, produkte, zahlung, lieferart)
        bestell_id = bestellung.erstelle_rechnung()

        session.pop("warenkorb", None)

        return render_template("rechnung.html", bestellung=bestellung)

    except NichtGefundenFehler as ng:
        return str(ng)

    except Exception as e:
        print("Fehler bei der Bestellung:", e)
        raise SpeicherFehler("Fehler beim Absenden der Bestellung.")

# Route to rate a product (1 to 5 stars)
@app.route("/bewerten", methods=["POST"])
def bewerten():
    # Nur eingeloggte Benutzer dürfen bewerten
    if "user" not in session:
        return redirect(url_for("login"))

    produkt_id = request.form.get("produkt_id")
    rating = request.form.get("rating")
    user_email = session.get("user")

    # Ungültige Eingaben – Ignorieren
    if not produkt_id or not rating or not user_email:
        return redirect(url_for("produkte_anzeigen"))

    try:
        produkt_id = int(produkt_id)
        rating = int(rating)

        if not 1 <= rating <= 5:
            raise ValueError("Bewertung muss zwischen 1 und 5 sein.")

        # Bewertung hinzufügen
        Produkt.add_review(produkt_id, rating, user_email)

    except ValueError as ve:
        print("Ungültige Bewertung:", ve)

    except SpeicherFehler as se:
        print("Speicherfehler beim Bewerten:", se)

    except Exception as e:
        print("Unbekannter Fehler beim Bewerten:", e)
        raise SpeicherFehler("Bewertung konnte nicht gespeichert werden.")

    return redirect(url_for("produkte_anzeigen"))
