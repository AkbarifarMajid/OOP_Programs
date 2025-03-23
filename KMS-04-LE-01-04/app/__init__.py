# app/__init__.py

from flask import Flask

app = Flask(__name__)
app.secret_key = "geheime_schluessel"  # برای Session و Flash پیام‌ها

from app import routes  # به فایل آدرس‌ها اشاره می‌کنه
