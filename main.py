from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import sql_queries as sql

# connect to the mysql database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Welkom01',
    database='library'
)

# create a cursor
cursor = conn.cursor()

# create fastAPI app
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",  # Update this with your Vue.js frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

books = sql.read_books(cursor)

@app.get("/books")
def read_books():
    return books


authors = sql.read_authors(cursor)

@app.get("/authors")
def read_authors():
    return authors

borrowings = sql.read_borrowings(cursor)

@app.get('/borrowings')
def read_borrowings():
    return borrowings

clients = sql.read_clients(cursor)

@app.get('/clients')
def read_clients():
    return clients


@app.post('/extended-borrowing')
async def extend_borrowing(id):
    sql.extend_borrowing(cursor, conn, id)
    return {'message': 'ID received succesfully'}

print(

sql.borrowing_is_overdue(cursor, 53)
)

# Close the mysql connection
cursor.close()
conn.close()