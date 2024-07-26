from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# configuration file for sql database
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///powerlifterdatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
