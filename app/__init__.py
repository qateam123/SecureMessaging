from flask import Flask
my_app = Flask(__name__)
from app.views import views
app.config.from_object('config')
