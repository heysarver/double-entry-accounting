from sqlalchemy.sql import text
from app import db

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Uuid, primary_key=True, default=text("gen_random_uuid()"))
    company_id = db.Column(db.Uuid, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Account(Base):
    __tablename__ = 'accounts'
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    normal = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': str(self.id),
            'company_id': str(self.company_id),
            'name': self.name,
            'number': self.number,
            'normal': self.normal
        }

class Transaction(Base):
    __tablename__ = 'transactions'
    txn_id = db.Column(db.String(36), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    currency = db.Column(db.String(8), nullable=False, default='USD')
    account_id = db.Column(db.Uuid, db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    # account_number = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.Integer, nullable=False)
    account = db.relationship('Account', backref=db.backref('transactions', lazy=True))

    def to_dict(self):
        return {
            'id': str(self.id),
            'company_id': str(self.company_id),
            'txn_id': self.txnid,
            'date': self.date,
            'amount': self.amount,
            'currency': self.currency,
            # 'account_number': self.account_number,
            'direction': self.account_number,
        }
