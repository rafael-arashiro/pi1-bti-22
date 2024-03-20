from flask import Flask
import mysql.connector
from flask_login import LoginManager

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='darkwhat16',
    database='pi_db'
)

app = Flask(__name__)
app.config.from_object('config')

from app.models import formulario
from app.controllers import default