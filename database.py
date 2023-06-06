import mysql.connector
from prettytable import PrettyTable

# connect to the mysql database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Welkom01',
    database='library'
)

# create a cursor
cursor = conn.cursor()

# crud functions for books


def create_book(book_id, title, publisher_id, genre_id, author_id):
    # for this function to work, the following requirements have to be satisfied:
    # - id's must be an integer, title must be a string
    # - publisher_id, genre_id and author_id must reference an existing publisher, genre and author
    values = book_id, title, publisher_id, genre_id, author_id
    # sql query
    insert_query = 'INSERT INTO books VALUES (%s, %s, %s, %s, %s)'
    # execute and commit
    cursor.execute(insert_query, values)
    conn.commit()


def read_books():
    select_query = "SELECT * FROM books"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # create table and print it in the terminal
    table = PrettyTable()
    table.field_names = ["Book ID", "Title",
                         "Publisher ID", "Genre ID", "Author ID"]
    for row in rows:
        table.add_row(row)
    print(table)

    return rows


def update_books(book_id, title, publisher_id, genre_id, author_id):
    update_query = "UPDATE books SET title = %s, publisher_id = %s, genre_id= %s, author_id = %s WHERE book_id = %s"
    values = (title, publisher_id, genre_id, author_id, book_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_book(book_id):
    delete_query = "DELETE FROM books WHERE book_id = %s"
    value = (book_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for author


def create_author(author_id, name, nationality):
    insert_query = "INSERT INTO authors VALUES (%s, %s, %s)"
    values = (author_id, name, nationality)
    cursor.execute(insert_query, values)
    conn.commit()


def read_authors():
    select_query = "SELECT * FROM authors"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # create table and print it in the terminal
    table = PrettyTable()
    table.field_names = ["Author ID", "Name", "Nationality"]
    for row in rows:
        table.add_row(row)
    print(table)

    return rows


def update_author(author_id, name, nationality):
    update_query = "UPDATE authors SET name = %s, nationality = %s WHERE author_id = %s"
    values = (name, nationality, author_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_author(author_id):
    delete_query = "DELETE FROM authors WHERE author_id = %s"
    value = (author_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for publishers


def create_publisher(publisher_id, name):
    insert_query = "INSERT INTO publishers VALUES (%s, %s)"
    values = (publisher_id, name)
    cursor.execute(insert_query, values)
    conn.commit()


def read_publishers():
    select_query = "SELECT * FROM publishers"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Publisher ID", "Name"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_publisher(publisher_id, name):
    update_query = "UPDATE publishers SET name = %s WHERE publisher_id = %s"
    values = (name, publisher_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_publisher(publisher_id):
    delete_query = "DELETE FROM publishers WHERE publisher_id = %s"
    value = (publisher_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for genres


def create_genre(genre_id, name):
    insert_query = "INSERT INTO genres VALUES (%s, %s)"
    values = (name, genre_id)
    cursor.execute(insert_query, values)
    conn.commit()


def read_genres():
    select_query = "SELECT * FROM genres"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Genre ID", "Name"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_genre(genre_id, name):
    update_query = "UPDATE genres SET name = %s WHERE genre_id = %s"
    values = (name, genre_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_genre(genre_id):
    delete_query = "DELETE FROM genres WHERE genre_id = %s"
    value = (genre_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for copies


def create_copy(copy_id, book_id, edition):
    insert_query = "INSERT INTO copies VALUES (%s, %s, %s)"
    values = (copy_id, book_id, edition)
    cursor.execute(insert_query, values)
    conn.commit()


def read_copies():
    select_query = "SELECT * FROM copies"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Copy ID", "Book ID", "Edition"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_copy(copy_id, book_id, edition):
    update_query = "UPDATE copies SET book_id = %s, edition = %s WHERE copy_id = %s"
    values = (book_id, edition, copy_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_copy(copy_id):
    delete_query = "DELETE FROM copies WHERE copy_id = %s"
    value = (copy_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for clients


def create_client(client_id, first_name, last_name, phone_number, street, house_nr, city, email_address):
    insert_query = "INSERT INTO clients VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (client_id, first_name, last_name, phone_number,
              street, house_nr, city, email_address)
    cursor.execute(insert_query, values)
    conn.commit()


def read_clients():
    select_query = "SELECT * FROM clients"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Client ID", "First Name", "Last Name",
                         "Phone Number", "Street", "House Nr", "City", "Email Address"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_client(client_id, first_name, last_name, phone_number, street, house_nr, city, email_address):
    update_query = "UPDATE clients SET first_name = %s, last_name = %s, phone_number = %s, street = %s, house_nr = %s, city = %s, email_address = %s WHERE client_id = %s"
    values = (first_name, last_name, phone_number, street,
              house_nr, city, email_address, client_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_client(client_id):
    delete_query = "DELETE FROM clients WHERE client_id = %s"
    value = (client_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for borrowings


def create_borrowing(borrowing_id, borrowing_date, is_extended, client_id, copy_id, return_id):
    insert_query = "INSERT INTO borrowings VALUES (%s, %s, %s, %s, %s, %s)"
    values = (borrowing_id, borrowing_date, is_extended,
              client_id, copy_id, return_id)
    cursor.execute(insert_query, values)
    conn.commit()


def read_borrowings():
    select_query = "SELECT * FROM borrowings"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Borrowing ID", "Borrowing Date",
                         "Is Extended", "Client ID", "Copy ID", "Return ID"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_borrowing(borrowing_id, borrowing_date, is_extended, client_id, copy_id, return_id):
    update_query = "UPDATE borrowings SET borrowing_date = %s, is_extended = %s, client_id = %s, copy_id = %s, return_id = %s WHERE borrowing_id = %s"
    values = (borrowing_date, is_extended, client_id,
              copy_id, return_id, borrowing_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_borrowing(borrowing_id):
    delete_query = "DELETE FROM borrowings WHERE borrowing_id = %s"
    value = (borrowing_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for returns


def create_return(return_id, return_date, condition):
    insert_query = "INSERT INTO returns VALUES (%s, %s, %s)"
    values = (return_date, condition)
    cursor.execute(insert_query, values)
    conn.commit()


def read_returns():
    select_query = "SELECT * FROM returns"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Return ID", "Return Date", "Condition"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_return(return_id, return_date, condition):
    update_query = "UPDATE returns SET return_date = %s, condition = %s WHERE return_id = %s"
    values = (return_date, condition, return_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_return(return_id):
    delete_query = "DELETE FROM returns WHERE return_id = %s"
    value = (return_id,)
    cursor.execute(delete_query, value)
    conn.commit()


# crud functions for bookauthor

def create_book_author(book_id, author_id, publication_date):
    insert_query = "INSERT INTO book_author VALUES (%s, %s, %s)"
    values = (book_id, author_id, publication_date)
    cursor.execute(insert_query, values)
    conn.commit()


def read_book_authors():
    select_query = "SELECT * FROM book_author"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Book ID", "Author ID", "Publication Date"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_book_author(book_id, author_id, publication_date):
    update_query = "UPDATE book_author SET publication_date = %s WHERE book_id = %s AND author_id = %s"
    values = (publication_date, book_id, author_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_book_author(book_id, author_id):
    delete_query = "DELETE FROM book_author WHERE book_id = %s AND author_id = %s"
    values = (book_id, author_id)
    cursor.execute(delete_query, values)
    conn.commit()


# create_book(9999, 'test', 60005, 50039, 70003)
delete_book(9999)
read_books()

# Close the connection
cursor.close()
conn.close()
