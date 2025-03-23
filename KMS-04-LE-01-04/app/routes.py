from flask import render_template, request, redirect, url_for, session
from app import app

from produkte.buch import Buch
from produkte.elektronik import Elektronik
from produkte.kleidung import Kleidung

@app.route("/")
def home():
    if "user" in session:
        return f"Willkommen zurück, {session['user']}!"
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == "majid@gmail.com" and password == "majid":
            session["user"] = email
            return redirect(url_for("home"))
        else:
            return "Login fehlgeschlagen!"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if name and email and password:
            return f"Registrierung erfolgreich für {name}!"
        else:
            return "Fehler: Bitte alle Felder ausfüllen."

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)  # حذف کلید "user" از session
    return redirect(url_for("login"))  # هدایت به صفحه ورود

@app.route("/produkte")
def produkte_anzeigen():
    if "user" not in session:
        return redirect(url_for("login"))

    buecher = Buch.get_all_books() or []
    elektro = Elektronik.get_all_electronics() or []
    kleider = Kleidung.get_all_clothing() or []

    produkte = []

    for b in buecher:
        produkte.append({"name": b[1], "price": b[2], "typ": "Buch"})
    for e in elektro:
        produkte.append({"name": e[1], "price": e[2], "typ": "Elektronik"})
    for k in kleider:
        produkte.append({"name": k[1], "price": k[2], "typ": "Kleidung"})

    return render_template("produkte.html", produkte=produkte)