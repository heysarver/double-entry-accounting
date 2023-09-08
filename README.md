# double-entry-accounting
A double-entry accounting system REST API implementation

Flask
PostgreSQL

Todo:
 - Documentation
 - Refactor app files
 - Fix create/update transaction pair to be a single request

Database modeled from https://blog.journalize.io/posts/an-elegant-db-schema-for-double-entry-accounting/

### Import Database Schema
```
flask --app=migrate.py db upgrade
```

### Load Test Data

Test data has a company ID of 00000000-dead-beef-cafe-000000000000
```
python import_test_data.py
```

### Delete Test Data
```
python delete_test_data.py
```
