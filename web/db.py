import sqlite3
from contextlib import closing
from main import app

def connect_database():
    return sqlite3.connect(app.config['DATABASE'])

def make_db():
    with closing(connect_database()) as db:
        with app.open_resource('db_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
