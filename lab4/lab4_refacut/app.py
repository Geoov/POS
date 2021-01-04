from config import *

from manager_routes import manager
from editor_routes import editor
from author_routes import author

app.register_blueprint(manager)
app.register_blueprint(editor)
app.register_blueprint(author)


@app.route('/api/library/login', methods=['POST'])
def login_in_account():
    mycursor = mysql.connection.cursor()

    email = request.json.get("email")
    pss = request.json.get("password")

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

        output = 'You just logged in as ' + session['role']
        return jsonify({'Authentification succesful! ': output}), 202
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


@app.route('/api/library/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)
