from config import *

from manager_routes import manager
from editor_routes import editor
from author_routes import author

app.register_blueprint(manager)
app.register_blueprint(editor)
app.register_blueprint(author)


# noinspection PyBroadException
@app.route('/api/library/login', methods=['POST'])
def login_in_account():
    global form_post
    form_post = 0
    mycursor = mysql.connection.cursor()

    try:
        if request.form.get('email'):
            form_post = 1
    finally:
        pass

    if form_post:
        email = request.form.get('email')
        pss = request.form.get('password')
    else:
        email = request.json['email']
        pss = request.json['password']

    sql_select_user = 'SELECT id, role_id FROM users WHERE email = %s and password = %s'
    val = (email, pss)
    mycursor.execute(sql_select_user, val)
    myresult = mycursor.fetchall()

    if len(myresult) > 0:
        session['id'] = myresult[0][0]
        session['logged_in'] = 1
        if myresult[0][1] == 0:
            session['role'] = 'MANAGER'
        elif myresult[0][1] == 1:
            session['role'] = 'EDITOR'
        elif myresult[0][1] == 2:
            session['role'] = 'AUTHOR'
        else:
            session['role'] = 'GUEST'

        if form_post:
            return jsonify({'role': session['role'],
                            'id': session['id']}), 202
        else:
            output = 'You just logged in as ' + session['role']
            return jsonify({'Authentification succesful! ': output}), 202
    else:
        if form_post:
            return jsonify(), 401
        else:
            output = 'Wrong credentials'
            return jsonify({'Authentification failed! ': output}), 401


@app.route('/api/library/books', methods=['GET'])
def get_all_books():

    global search_attr, search_value

    mycursor = mysql.connection.cursor()

    if request.args.get('title') or request.args.get('genre') or request.args.get('year'):
        if request.args.get('title'):
            search_attr = 'title'
            search_value = '%'+request.args.get('title')+'%'
        if request.args.get('genre'):
            search_attr = 'genre'
            search_value = '%'+request.args.get('genre')+'%'
        if request.args.get('year'):
            search_attr = 'year'
            search_value = '%'+request.args.get('year')+'%'

        sql_select_all_books = 'SELECT books.title, CONCAT(users.first_name, \" \", users.last_name) author_name, ' \
                               'books.genre, books.year FROM users, books WHERE users.id = books.author_id AND ' \
                               'users.role_id = 2 AND books.{0} LIKE \'{1}\''.format(search_attr, str(search_value))
        mycursor.execute(sql_select_all_books)
    else:
        sql_select_all_books = 'SELECT books.title, CONCAT(users.first_name, " ", users.last_name) author_name, ' \
                               'books.genre, books.year FROM users, books WHERE users.id = books.author_id ' \
                               'AND users.role_id = 2'

        mycursor.execute(sql_select_all_books)

    myresult = mycursor.fetchall()
    output = []

    for res in myresult:
        output.append({'title': res[0], 'author name': res[1], 'book genre': res[2], 'book year': res[3]})
    return jsonify({'Books are ': output}), 200


# noinspection PyBroadException
@app.route('/api/library/books/<book_id>', methods=['GET'])
def get_book(book_id):
    mycursor = mysql.connection.cursor()

    global form_post
    form_post = 0

    try:
        if request.form.get('book_id'):
            form_post = 1
    finally:
        pass

    if form_post:
        book_id = request.form.get('book_id')

    sql_select_book = 'SELECT books.title, CONCAT(users.first_name, " ", users.last_name) author_name, ' \
                      'books.genre, books.year, books.author_id FROM users, books WHERE users.id = books.author_id ' \
                      'AND users.role_id = 2 AND books.id = %s'

    mycursor.execute(sql_select_book, (book_id,))

    myresult = mycursor.fetchall()
    output = []

    if myresult:
        for res in myresult:
            output.append({'title': res[0], 'author_name': res[1], 'book_genre': res[2], 'book_year': res[3],
                           'author_id': res[4]}), 200

        return jsonify({'book': output}), 200
    else:
        return jsonify({'book doesn\'t exist': None}), 404


@app.route('/api/library/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)
