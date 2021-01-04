from config import *

editor = Blueprint('editor_routes', __name__, template_folder="templates")

# noinspection PyBroadException
@editor.route('/api/library/books/requestEditBooks', methods=['GET'])
def get_request_edit_books():
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'EDITOR':
        sql_select_books_requested_to_edit = 'SELECT books.id, books.title, books.genre, books.year,' \
                                             'books_edited.title, books_edited.genre, books_edited.year FROM books, ' \
                                             'books_edited, users WHERE books.editor_id = users.id AND books.id = ' \
                                             'books_edited.book_id AND status LIKE "request_changes"'
        mycursor.execute(sql_select_books_requested_to_edit)

        myresult = mycursor.fetchall()

        output = []

        for res in myresult:
            output.append({'Id_book': res[0], 'Book title': res[1], 'Genre': res[2], 'Year': res[3],
                           'Requested book title': res[4], 'Requested book genre': res[5],
                           'Requested book year': res[6]})
        return jsonify({'Requesting edit books are': output}), 200
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection PyBroadException
@editor.route('/api/library/books', methods=['POST'])
def insert_book():
    mycursor = mysql.connection.cursor()

    global form_post, author, editor_id, title, genre, year
    form_post = 0

    try:
        if request.form.get('title') and request.form.get('author'):
            form_post = 1
    finally:
        pass

    if form_post:
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        year = request.form.get('year')
        editor_id = request.form.get('editor_id')
        role = 'EDITOR'
    else:
        try:
            is_logged = session['logged_in']
        except:
            is_logged = 0

        if is_logged == 0:
            session['role'] = 'GUEST'

        role = session['role']

    if role == 'EDITOR':
        if form_post == 0:
            title = request.json['title']
            author = request.json['author']
            genre = request.json['genre']
            year = request.json['year']
            editor_id = session['id']

        sql_insert_book = 'INSERT INTO books(author_id, editor_id, title, genre, year, status) VALUES ' \
                          '(%s, %s, %s, %s, %s, %s)'
        mycursor.execute(sql_insert_book, (author, editor_id, title, genre, year, 'approved'))

        sql_select_last_id = 'SELECT LAST_INSERT_ID()'
        mycursor.execute(sql_select_last_id)

        myresult = mycursor.fetchall()

        mysql.connection.commit()

        output = 'Book inserted with id: ' + str(myresult[0][0])
        return jsonify({'Successful inserted book': output}), 201
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection PyBroadException
@editor.route('/api/library/books/<book_id>', methods=['PATCH'])
def update_author_book(book_id):
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'EDITOR':

        sql_select_book = 'SELECT books.id, books.author_id, books.title, books.genre, books.year FROM books WHERE ' \
                          'books.id = %s'
        mycursor.execute(sql_select_book, (book_id,))

        myresult = mycursor.fetchall()

        if myresult:
            req = request.data
            try:
                req_json = json.loads(req.decode('utf8').replace("'", '"'))
            except:
                req_json = ""

            try:
                author_id = req_json['author']
            except:
                author_id = myresult[0][1]

            sql_select_author = 'SELECT users.id FROM users WHERE users.id = %s AND users.role_id = %s'
            mycursor.execute(sql_select_author, (author_id, 2))

            check_if_author = mycursor.fetchall()

            if check_if_author:
                sql_insert_book = 'UPDATE books SET author_id = %s WHERE id=%s'
                mycursor.execute(sql_insert_book, (author_id, book_id))

                mycursor.fetchall()

                mysql.connection.commit()

                output = 'Book with id: ' + str(book_id) + ' has now author with id: ' + str(author_id)
                return jsonify({'Succesful update!': output}), 200
            else:
                output = 'Author with id: ' + str(author_id) + ' doesn\'t exist'
                return jsonify({'Failed update!': output}), 404
        else:
            output = 'Book with id: ' + book_id + ' doesn\'t exist'
            return jsonify({'Failed update!': output}), 404
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection PyBroadException
@editor.route('/api/library/books/requestEditBooks/<book_id>', methods=['PUT'])
def update_request_book(book_id):
    global edited_title, edited_genre, edited_year
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'EDITOR':

        sql_select_book = 'SELECT books.id, books.author_id, books.title, books.genre, books.year FROM books WHERE ' \
                          'books.id = %s AND books.status LIKE "request_changes"'
        mycursor.execute(sql_select_book, (book_id,))

        myresult = mycursor.fetchall()

        if myresult:
            try:
                req = request.data
                req_json = json.loads(req.decode('utf8').replace("'", '"'))
            except:
                req_json = ''

            try:
                status_edit = req_json['status']
            except:
                status_edit = 'rejected'

            sql_update_status_book = 'UPDATE books SET status = %s'
            mycursor.execute(sql_update_status_book, (status_edit,))

            mycursor.fetchall()

            mysql.connection.commit()

            if status_edit == 'approved':
                sql_select_requested_books_edit = 'SELECT books_edited.title, books_edited.genre, books_edited.year ' \
                                                  'FROM books_edited WHERE books_edited.book_id = %s'
                mycursor.execute(sql_select_requested_books_edit, (book_id,))

                myresult_edited = mycursor.fetchall()
                for _ in myresult_edited:
                    edited_title = myresult_edited[0][0]
                    edited_genre = myresult_edited[0][1]
                    edited_year = myresult_edited[0][2]

                sql_update_book = 'UPDATE books SET title = %s, genre = %s, year = %s WHERE id = %s'
                mycursor.execute(sql_update_book, (edited_title, edited_genre, edited_year, book_id))

                mycursor.fetchall()

                mysql.connection.commit()

                sql_delete_requested_book = 'DELETE FROM books_edited WHERE book_id = %s'
                mycursor.execute(sql_delete_requested_book, (book_id,))

                mysql.connection.commit()

                output = 'Book with id: ' + str(book_id) + ' is now set on approved'
                return jsonify({'Succesful update!': output}), 200

            else:
                output = 'Book with id: ' + str(book_id) + ' is now set on rejected'
                return jsonify({'Succesful update!': output}), 200
        else:
            output = 'Book with id: ' + book_id + ' doesn\'t request changes'
            return jsonify({'Failed update!': output}), 404
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection PyBroadException
@editor.route('/api/library/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'EDITOR':
        sql_delete_user = 'DELETE FROM books WHERE id = %s'
        res = mycursor.execute(sql_delete_user, (book_id,))

        mysql.connection.commit()

        if res:
            output = 'Book with id ' + book_id + ' deleted'
            return jsonify({'Delete successful! ': output}), 202
        else:
            output = 'Book with id ' + book_id + ' doesn\'t exit'
            return jsonify({'Delete failed! ': output}), 404
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403
