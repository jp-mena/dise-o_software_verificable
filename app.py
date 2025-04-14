# app.py

from flask import Flask
from flask_mysqldb import MySQL
import db_config

app = Flask(__name__)

# Configuración desde db_config
app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
app.config['MYSQL_USER'] = db_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = db_config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def index():
    return '¡Sistema de Gestión Académica funcionando!'

if __name__ == '__main__':
    app.run(debug=True)
