from prettytable import PrettyTable
from datetime import datetime, timedelta

today = datetime.now().date()

# crud functions for books


def create_book(cursor, conn, book_id, title, publisher_id, genre_id, author_id):
    # for this function to work, the following requirements have to be satisfied:
    # - id's must be an integer, title must be a string
    # - publisher_id, genre_id and author_id must reference an existing publisher, genre and author
    values = book_id, title, publisher_id, genre_id, author_id
    # sql query
    insert_query = 'INSERT INTO books VALUES (%s, %s, %s, %s, %s)'
    # execute and commit
    cursor.execute(insert_query, values)
    conn.commit()


def read_books(cursor):
    select_query = f"select * from books"
    cursor.execute(select_query)
    fetches = cursor.fetchall()
    
    books = [{'book_id': fetch[0], 'title': fetch[1], 'publisher_id': fetch[2], 'genre_id': fetch[3], 'publication_date': fetch[4]} for fetch in fetches]

    for book in books:
    # # insert author name and delete author id from the book dictionaries
        author_names = read_author_names(cursor, book['book_id'])
        book['authors'] = author_names

        publisher_name = read_publisher_name(cursor, book['publisher_id'])
        book['publisher'] = publisher_name
        del book['publisher_id']

        genre_name = read_genre_name(cursor, book['genre_id'])
        book['genre'] = genre_name
        del book['genre_id']

        copy_amount = read_copy_amount(cursor, book['book_id'])
        book['copies'] = copy_amount

        copy_editions = read_copy_editions(cursor, book['book_id'])
        book['editions'] = copy_editions
                 
    return books

def read_book_by_copy_id(cursor, id):
    select_query = f"select a.title from books a left join copies b on a.book_id = b.book_id where b.copy_id = {id}"
    cursor.execute(select_query)
    title = cursor.fetchall()[0][0]
    
    return title



def update_books(cursor, conn, book_id, title, publisher_id, genre_id, author_id):
    update_query = "UPDATE books SET title = %s, publisher_id = %s, genre_id= %s, author_id = %s WHERE book_id = %s"
    values = (title, publisher_id, genre_id, author_id, book_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_book(cursor, conn, book_id):
    delete_query = "DELETE FROM books WHERE book_id = %s"
    value = (book_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for author


def create_author(cursor, conn, author_id, name, nationality):
    insert_query = "INSERT INTO authors VALUES (%s, %s, %s)"
    values = (author_id, name, nationality)
    cursor.execute(insert_query, values)
    conn.commit()


def read_authors(cursor):
    select_query = f"SELECT * FROM authors"
    cursor.execute(select_query)
    fetches = cursor.fetchall()

    authors = [{'author_id': fetch[0], 'name': fetch[1], 'nationality': fetch[2]} for fetch in fetches]

    for author in authors:
        books = read_author_books(cursor, author['author_id'])
        author['books'] = books

    return authors

def read_author_names(cursor, book_id):
    select_query = f"SELECT a.name FROM authors a LEFT JOIN book_author b ON a.author_id = b.author_id LEFT JOIN books c ON b.book_id = c.book_id where c.book_id = {book_id}"
    cursor.execute(select_query)
    fetched_names = cursor.fetchall()
    names = []

    for name in fetched_names:
        names.append(name[0])

    return names

def read_author_books(cursor, id):
    select_query = f"select a.title from books a left join book_author b on a.book_id = b.book_id left join authors c on b.author_id = c.author_id where c.author_id = {id}"
    cursor.execute(select_query)
    fetched_titles = cursor.fetchall()

    titles = list(set([title[0] for title in fetched_titles]))

    return titles



def update_author(cursor, conn, author_id, name, nationality):
    update_query = "UPDATE authors SET name = %s, nationality = %s WHERE author_id = %s"
    values = (name, nationality, author_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_author(cursor, conn, author_id):
    delete_query = "DELETE FROM authors WHERE author_id = %s"
    value = (author_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for publishers


def create_publisher(cursor, conn, publisher_id, name):
    insert_query = "INSERT INTO publishers VALUES (%s, %s)"
    values = (publisher_id, name)
    cursor.execute(insert_query, values)
    conn.commit()


def read_publisher_name(cursor, id):
    # select publisher name by id
    select_query = f"SELECT name FROM publishers where publisher_id = {id}"
    cursor.execute(select_query)
    name = cursor.fetchall()[0][0]
    
    return name


def update_publisher(cursor, conn, publisher_id, name):
    update_query = "UPDATE publishers SET name = %s WHERE publisher_id = %s"
    values = (name, publisher_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_publisher(cursor, conn, publisher_id):
    delete_query = "DELETE FROM publishers WHERE publisher_id = %s"
    value = (publisher_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for genres


def create_genre(cursor, conn, genre_id, name):
    insert_query = "INSERT INTO genres VALUES (%s, %s)"
    values = (name, genre_id)
    cursor.execute(insert_query, values)
    conn.commit()


def read_genre_name(cursor, id):
    select_query = f"SELECT name FROM genres where genre_id = {id}"
    cursor.execute(select_query)
    name = cursor.fetchall()[0][0]

    return name

def update_genre(cursor, conn, genre_id, name):
    update_query = "UPDATE genres SET name = %s WHERE genre_id = %s"
    values = (name, genre_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_genre(cursor, conn, genre_id):
    delete_query = "DELETE FROM genres WHERE genre_id = %s"
    value = (genre_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for copies


def create_copy(cursor, conn, copy_id, book_id, edition):
    insert_query = "INSERT INTO copies VALUES (%s, %s, %s)"
    values = (copy_id, book_id, edition)
    cursor.execute(insert_query, values)
    conn.commit()


def read_copy_ids(cursor):
    select_query = "SELECT copy_id FROM copies"
    cursor.execute(select_query)
    fetched_copies = cursor.fetchall()

    copies = [item[0] for item in fetched_copies]

    return copies

def read_borrowed_copies(cursor):
    select_query = "SELECT copy_id, return_id FROM borrowings"
    cursor.execute(select_query)
    fetched_copies = cursor.fetchall()

    copies = [item[0] for item in fetched_copies if item[1] is None]

    return copies



def read_copy_amount(cursor, id):
    select_query = f"SELECT count(*) FROM copies WHERE book_id = {id}"
    cursor.execute(select_query)
    amount = cursor.fetchall()[0][0]

    return amount

def read_copy_editions(cursor, id):
    select_query = f"SELECT edition FROM copies WHERE book_id = {id}"
    cursor.execute(select_query)
    fetched_editions = cursor.fetchall()

    editions = list(set([edition[0] for edition in fetched_editions]))

    return editions


def update_copy(cursor, conn, copy_id, book_id, edition):
    update_query = "UPDATE copies SET book_id = %s, edition = %s WHERE copy_id = %s"
    values = (book_id, edition, copy_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_copy(cursor, conn, copy_id):
    delete_query = "DELETE FROM copies WHERE copy_id = %s"
    value = (copy_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for clients


def create_client(cursor, conn, client_id, first_name, last_name, phone_number, street, house_nr, city, email_address):
    insert_query = "INSERT INTO clients VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (client_id, first_name, last_name, phone_number,
              street, house_nr, city, email_address)
    cursor.execute(insert_query, values)
    conn.commit()

def read_clients(cursor):
    select_query = "SELECT * FROM clients"
    cursor.execute(select_query)
    fetched_clients = cursor.fetchall()

    clients = [{'client_id': item[0], 'first_name': item[1], 'last_name': item[2], 'phone_number': item[3], 'street': item[4], 'house_nr': item[5], 'city': item[6], 'email_address': item[7]} for item in fetched_clients]

    # print(clients[0])

    for client in clients:
        # add return date
        address = f'{client["street"]} {client["house_nr"]}, {client["city"]}'
        client['address'] = address
        del client['street']
        del client['house_nr']
        del client['city']     

        # add name
        name = f'{client["first_name"]} {client["last_name"]}'
        client['name'] = name
        del client['first_name']
        del client['last_name']

        # add has overdue borrowings
        has_overdue_borrowings = 'n'
        borrowing_ids = read_borrowing_ids(cursor, client['client_id'])
        for id in borrowing_ids:
            is_overdue = borrowing_is_overdue(cursor, id)
            if (is_overdue == 'y'): has_overdue_borrowings = 'y'

        client['has_overdue_borrowings'] = has_overdue_borrowings


    return clients

# def read_clients(cursor):
#     select_query = "SELECT * FROM clients"
#     cursor.execute(select_query)
#     rows = cursor.fetchall()

#     table = PrettyTable()
#     table.field_names = ["Client ID", "First Name", "Last Name",
#                          "Phone Number", "Street", "House Nr", "City", "Email Address"]
#     for row in rows:
#         table.add_row(row)
#     print(table)


def update_client(cursor, conn, client_id, first_name, last_name, phone_number, street, house_nr, city, email_address):
    update_query = "UPDATE clients SET first_name = %s, last_name = %s, phone_number = %s, street = %s, house_nr = %s, city = %s, email_address = %s WHERE client_id = %s"
    values = (first_name, last_name, phone_number, street,
              house_nr, city, email_address, client_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_client(cursor, conn, client_id):
    delete_query = "DELETE FROM clients WHERE client_id = %s"
    value = (client_id,)
    cursor.execute(delete_query, value)
    conn.commit()

# crud functions for borrowings


def create_borrowing(cursor, conn, borrowing_id, borrowing_date, is_extended, client_id, copy_id, return_id):
    insert_query = "INSERT INTO borrowings VALUES (%s, %s, %s, %s, %s, %s)"
    values = (borrowing_id, borrowing_date, is_extended,
              client_id, copy_id, return_id)
    cursor.execute(insert_query, values)
    conn.commit()


def read_borrowings(cursor):
    select_query = "SELECT * FROM borrowings"
    cursor.execute(select_query)
    fetched_borrowings = cursor.fetchall()

    borrowings = [{'borrowing_id': item[0], 'copy_id': item[4], 'borrowing_date': item[1], 'is_extended': item[2], 'client_id': item[3], 'return_id': item[5]} for item in fetched_borrowings]

    for borrowing in borrowings:
        # add due date
        date = borrowing['borrowing_date']
        # Add 7/14 days to the date
        borrowing_length = 14 if borrowing["is_extended"] == 'y' else 7
        new_date = date + timedelta(days=borrowing_length)
        borrowing['due_date'] = new_date

        # add book title
        book_title = read_book_by_copy_id(cursor, borrowing['copy_id'])
        borrowing['book'] = book_title

        # add can_be_extended
        can_be_extended = 'n'
        seven_days_ago = today - timedelta(days=7)
        if (borrowing["borrowing_date"] > seven_days_ago and borrowing['return_id'] is None and borrowing['is_extended'] == 'n'):
            can_be_extended = 'y'
        borrowing['can_be_extended'] = can_be_extended

        # add is overdue
        is_overdue = 'n'
        if (today > borrowing['due_date'] and borrowing['return_id'] == None):
            is_overdue = 'y'
        borrowing['is_overdue'] = is_overdue

    return borrowings

def update_borrowing( cursor, conn, borrowing_id, borrowing_date, is_extended, client_id, copy_id, return_id):
    update_query = "UPDATE borrowings SET borrowing_date = %s, is_extended = %s, client_id = %s, copy_id = %s, return_id = %s WHERE borrowing_id = %s"
    values = (borrowing_date, is_extended, client_id,
              copy_id, return_id, borrowing_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_borrowing(cursor, conn, borrowing_id):
    delete_query = "DELETE FROM borrowings WHERE borrowing_id = %s"
    value = (borrowing_id,)
    cursor.execute(delete_query, value)
    conn.commit()

def extend_borrowing(cursor, conn, id):
    extend_query = f"update borrowings set is_extended = 'y' where borrowing_id = {id}"
    cursor.execute(extend_query)
    conn.commit()

# crud functions for returns


def create_return(cursor, conn, return_id, return_date, condition):
    insert_query = "INSERT INTO returns VALUES (%s, %s, %s)"
    values = (return_date, condition)
    cursor.execute(insert_query, values)
    conn.commit()


def read_returns(cursor):
    select_query = "SELECT * FROM returns"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Return ID", "Return Date", "Condition"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_return(cursor, conn, return_id, return_date, condition):
    update_query = "UPDATE returns SET return_date = %s, condition = %s WHERE return_id = %s"
    values = (return_date, condition, return_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_return(cursor, conn, return_id):
    delete_query = "DELETE FROM returns WHERE return_id = %s"
    value = (return_id,)
    cursor.execute(delete_query, value)
    conn.commit()


# crud functions for bookauthor

def create_book_author(cursor, conn, book_id, author_id, publication_date):
    insert_query = "INSERT INTO book_author VALUES (%s, %s, %s)"
    values = (book_id, author_id, publication_date)
    cursor.execute(insert_query, values)
    conn.commit()


def read_book_authors(cursor):
    select_query = "SELECT * FROM book_author"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Book ID", "Author ID", "Publication Date"]
    for row in rows:
        table.add_row(row)
    print(table)


def update_book_author(cursor, conn, book_id, author_id, publication_date):
    update_query = "UPDATE book_author SET publication_date = %s WHERE book_id = %s AND author_id = %s"
    values = (publication_date, book_id, author_id)
    cursor.execute(update_query, values)
    conn.commit()


def delete_book_author(cursor, conn, book_id, author_id):
    delete_query = "DELETE FROM book_author WHERE book_id = %s AND author_id = %s"
    values = (book_id, author_id)
    cursor.execute(delete_query, values)
    conn.commit()

def read_borrowing_ids(cursor, id):
    select_query = f"SELECT borrowing_id FROM borrowings where client_id = {id}"
    cursor.execute(select_query)
    fetched_ids = cursor.fetchall()

    borrowing_ids = [id[0] for id in fetched_ids]

    return borrowing_ids

def borrowing_is_overdue(cursor, id):
    select_query = f"SELECT borrowing_date, is_extended, return_id FROM borrowings where borrowing_id = {id}"
    cursor.execute(select_query)
    fetched_data = cursor.fetchall()

    borrowing_date = fetched_data[0][0]
    is_extended = fetched_data[0][1]
    is_returned = fetched_data[0][2]
    seven_days = timedelta(days=7)
    fourteen_days = timedelta(days=14)

    due_date = borrowing_date + fourteen_days if is_extended == 'y' else borrowing_date + seven_days

    if (is_returned == None and due_date < today): return 'y'
    return 'n'
