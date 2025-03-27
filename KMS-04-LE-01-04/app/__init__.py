# Initialisiert die Flask-App, setzt den geheimen Schlüssel und lädt die

from flask import Flask

app = Flask(__name__)
app.secret_key = "Akbarifar6503"

# zeigt auf die Adressdatei
from app import routes
