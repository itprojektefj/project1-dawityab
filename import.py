import sqlite3
import requests
import csv
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy
from application import app
db = SQLAlchemy(app)
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "9781632168146"})

_tablename__ = "books"
isbn = db.Column('isbn', db.String(50), primary_key=True)
title = db.Column('title', db.String(100), unique=False)
author = db.Column('author', db.String(50), unique=False)
year = db.Column('year', db.Integer,unique=False)
user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False)

def __init__(self, isbn, title, author, year):
            self.isbn = isbn
            self.title = title
            self.author = author
            self.year = year

def __repr__(self):
            return '<Books %r>' %(self.title)
with open('C:/Users/Fazehann/Desktop/project1/books.csv', 'r') as f:
    app.config['SECRET_KEY'] = 'r\x86/\x1d\x92\xa7\x043\x02\x97\xc6\xee\xf8\xaf\x07\x97'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/sqlite/reader.db'

    db = SQLAlchemy(app)

    #Defining database location
    #engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    reader = csv.reader(f)
    columns = next(reader)
    query = 'replace into books({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    for data in reader:
        cursor.execute(query, data)
    connection.commit()


