
from flask import Flask
import mysql
import mysql.connector

DATABASE = {
    'user': 'root',
    'password': 'my-secret-pw',
    'host': '173.17.0.7',
    'port': '3306',
    'database': 'AdoptAnimals'
}

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port'],
            database=DATABASE['database']
        )
    return db
