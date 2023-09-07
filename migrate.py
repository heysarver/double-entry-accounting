from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_NAME = os.getenv('POSTGRES_NAME', 'mydb')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# class Account(db.Model):
#     __tablename__ = 'accounts'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text)
#     number = db.Column(db.Integer)
#     normal = db.Column(db.Integer)
#     number_mod_100 = db.Column(db.Integer)
#     account_div_100_mul_100 = db.Column(db.Integer)

#     def __init__(self, name, number, normal, number_mod_100, account_div_100_mul_100):
#         self.name = name
#         self.number = number
#         self.normal = normal
#         self.number_mod_100 = number_mod_100
#         self.account_div_100_mul_100 = account_div_100_mul_100

#     def __repr__(self):
#         return f"<Account {self.id}>"


# class Transaction(db.Model):
#     __tablename__ = 'transactions'

#     id = db.Column(db.Integer, primary_key=True)
#     txnid = db.Column(db.Integer)
#     date = db.Column(db.Text)
#     amount = db.Column(db.Float)
#     account = db.Column(db.Integer)
#     direction = db.Column(db.Integer)

#     def __init__(self, txnid, date, amount, account, direction):
#         self.txnid = txnid
#         self.date = date
#         self.amount = amount
#         self.account = account
#         self.direction = direction

#     def __repr__(self):
#         return f"<Transaction {self.id}>"
