# Initializes the Flask app, sets the secret key and loads the
from flask import Flask

# points to the address file
from app import routes

app = Flask(__name__)
app.secret_key = "Akbarifar6503"

