from flask import Flask
app = Flask(__name__)
from app.views import views
app.config.from_pyfile('config.py')
