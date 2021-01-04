from config import *

author = Blueprint('author_routes', __name__, template_folder="templates")


# noinspection PyBroadException
@author.route('/api/library/books/myBooks', methods=['GET'])
def get_your_books():
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'AUTHOR':
        sql_select_books = 'SELECT books.id, CONCAT(users.first_name, " ", users.last_name), books.title, ' \
                           'books.genre, books.year, books.status FROM books, users WHERE books.author_id = %s ' \
                           'AND books.editor_id = users.id AND status != "request_changes"'

        mycursor.execute(sql_select_books, (session['id'],))

        myresult = mycursor.fetchall()

        output = []

        for res in myresult:
            output.append(
                {'Id_book': res[0], 'Editor name': res[1], 'Book title': res[2], 'Genre': res[3], 'Year': res[4],
                 'Status': res[5]})
        return jsonify({'Your books are': output}), 200
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection PyBroadException
@author.route('/api/library/books/myBooks/<book_id>', methods=['PUT'])
def modify_book(book_id):
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'AUTHOR':
        sql_select_book = 'SELECT books.id, CONCAT(users.first_name, " ", users.last_name), books.title,' \
                          ' books.genre, books.year FROM books, users WHERE ' \
                          'books.author_id = %s AND books.editor_id = users.id AND books.id = %s'
        mycursor.execute(sql_select_book, (session['id'], book_id))

        myresult = mycursor.fetchall()

        if myresult:
            req = request.data
            req_json = json.loads(req.decode('utf8').replace("'", '"'))

            try:
                title = req_json['title']
            except:
                title = myresult[0][2]
            try:
                genre = req_json['genre']
            except:
                genre = myresult[0][3]
            try:
                year = req_json['year']
            except:
                year = myresult[0][4]

            sql_insert_edit_book = 'INSERT INTO books_edited(book_id, title, genre, year) VALUES (%s, %s, %s, %s)' \
                                   ' ON DUPLICATE KEY UPDATE title = %s, genre = %s, year = %s'
            mycursor.execute(sql_insert_edit_book, (book_id, title, genre, year, title, genre, year))
            mysql.connection.commit()

            sql_update_author_book = 'UPDATE books SET status = "request_changes" WHERE id = %s'
            mycursor.execute(sql_update_author_book, (book_id,))
            mysql.connection.commit()

            output = 'Book with id: ' + book_id + ' is now updating'
            return jsonify({'Succesful request update!': output}), 202  # 202 pentru ca nu e terminata inca cererea
        else:
            output = 'Book with id: ' + book_id + ' doesn\'t exist'
            return jsonify({'Failed update!': output}), 404
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403
