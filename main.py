from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Boolean, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import mysql.connector
import sql_queries as sql

###################

# Create a SQLAlchemy engine
engine = create_engine("mysql+mysqlconnector://root:Welkom01@localhost/library")
SessionLocal = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define your model
class Borrowing(Base):
    __tablename__ = "borrowings"
    borrowing_id = Column(Integer, primary_key=True)
    is_overdue = Column(Boolean)

#########################

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

print(

sql.read_borrowed_copies(cursor)
)

all_copies = sql.read_copy_ids(cursor)
borrowed_copies = sql.read_borrowed_copies(cursor)
available_copies = [x for x in all_copies if x not in borrowed_copies]

@app.get('/available_copies')
def read_available_copies():
    return available_copies


@app.patch("/borrowings/{borrowing_id}")
async def update_borrowing(borrowing_id: int, is_extended: bool):
    # Create a database session
    db = SessionLocal()

    # Retrieve the borrowing record by borrowing_id
    borrowing = db.query(Borrowing).filter_by(borrowing_id=borrowing_id).first()

    if borrowing:
        # Update the is_overdue field
        borrowing.is_extended = 'y' if is_extended else 'n'
        db.commit()
        return {"message": "Borrowing updated successfully"}

    return {"message": "Borrowing not found"}




# @app.post('/extended-borrowing')
# async def extend_borrowing(id):
#     sql.extend_borrowing(cursor, conn, id)
#     return {'message': 'ID received succesfully'}

# Close the mysql connection
cursor.close()
conn.close()