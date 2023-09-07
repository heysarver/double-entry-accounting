from app import create_app, db
from app.models import Account, Transaction

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        tables = [Transaction, Account]
        for table in tables:
            num_deleted = db.session.query(table).filter(table.company_id == '00000000-dead-beef-cafe-000000000000').delete()
            db.session.commit()
            print(f"Cleared {num_deleted} records from the {table.__tablename__} table")
