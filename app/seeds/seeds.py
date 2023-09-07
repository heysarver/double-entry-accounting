from flask_seeder import Seeder
from app.models import Account, Transaction

class AccountSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1
    
    def run(self):
        accounts = [
            Account(name='Assets', number='100', normal='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Cash', number='110', normal='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Merchandise', number='120', normal='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Liabilities', number='200', normal='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Deferred Revenue', number='210', normal='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Revenues', number='300', normal='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Expenses', number='400', normal='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Cost of Goods Sold', number='410', normal='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Equity', number='500', normal='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Account(name='Capital', number='510', normal='-1', company_id='00000000-dead-beef-cafe-000000000000'),
        ]
        for account in accounts:
            self.db.session.add(account)

        self.db.session.flush()

        self.db.session.commit()

class TransactionSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2
    
    def run(self):
        accounts = self.db.session.query(Account).filter(Account.company_id == '00000000-dead-beef-cafe-000000000000').all()

        def select_account(account_number):
            for account in accounts:
                if account.number == account_number:
                    return account
            return None

        transactions = [
            Transaction(txn_id='00000000-0000-0000-0000-000000000000', date='2023-01-01', amount=50000, currency='USD', account=select_account(110), direction='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000000', date='2023-01-01', amount=50000, currency='USD', account=select_account(510), direction='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000001', date='2023-01-01', amount=10000, currency='USD', account=select_account(120), direction='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000001', date='2023-01-01', amount=10000, currency='USD', account=select_account(110), direction='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000002', date='2023-02-01', amount=1500, currency='USD', account=select_account(110), direction='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000002', date='2023-02-01', amount=1500, currency='USD', account=select_account(210), direction='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000003', date='2023-02-05', amount=1500, currency='USD', account=select_account(210), direction='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000003', date='2023-02-05', amount=1500, currency='USD', account=select_account(300), direction='-1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000004', date='2023-02-05', amount=300, currency='USD', account=select_account(410), direction='1', company_id='00000000-dead-beef-cafe-000000000000'),
            Transaction(txn_id='00000000-0000-0000-0000-000000000004', date='2023-02-05', amount=300, currency='USD', account=select_account(120), direction='-1', company_id='00000000-dead-beef-cafe-000000000000'),
        ]

        for transaction in transactions:
            self.db.session.add(transaction)

        self.db.session.flush()

        self.db.session.commit()
