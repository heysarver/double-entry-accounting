# accounting-api
A double-entry ledger API implementation

Database modeled from https://blog.journalize.io/posts/an-elegant-db-schema-for-double-entry-accounting/

```
flask --app=migrate.py db init
```

```
flask --app=migrate.py db migrate
flask --app=migrate.py db upgrade
```
