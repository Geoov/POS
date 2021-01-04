from config import *

from manager_routes import manager
from editor_routes import editor
from author_routes import author

app.register_blueprint(manager)
app.register_blueprint(editor)
app.register_blueprint(author)

jwt = JWTManager(app)


@app.route('/api/library/login', methods=['POST'])
# @jwt_required
def login_in_account():
    auth_token = request.headers.get('Authorization')
    cookie = request.headers.get('Cookie')

    if not auth_token or not cookie:
        return jsonify({'Not Authorized ': "Missing cookie or JWT Token"}), 401

    wsdl = 'http://localhost:8080/ws/login.wsdl'
    client = Client(wsdl)

    ##### cu suds.client

    ### merge facand mai nimic

    #####

    ####### incercari cu zeep

    ### initial imi dadea method not found cu toate ca era mapata in python3 -m zeep .../8080/ws/login.wsdl
    ### aparent aveau prefix ns0 si credeam ca e de aici dar, de fapt, era ca trebuia sau functia care s-a
    ### creat in XmlRoot (getUserRole) si nu cea care e obiect (getUserRoleRequest)

    # client.set_ns_prefix("ns0", "http://localhost:5000/api/library/users")
    # factory = client.type_factory('ns0')

    ### dadea exceptia la parsarea xml-ului si am incercat prin binding ceva si prin strict mode = False dar n-a mers..

    # response = pretend.stub(
    # status_code=200,
    # headers={cookie, auth_token},
    # content="""
    #     <!-- The response from the server -->
    # """)

    # operation = client.service._binding._operations['getUserRole']
    # result = client.service._binding.process_reply(
    #     client, operation, response)

    # operation = client.service.getUserRole(cookie=cookie, token=auth_token)

    # result = client.service._binding.process_reply(
    #     client, operation, response)

    # client.settings(strict=False)

    #######

    result = client.service.getUserRole(cookie=cookie, token=auth_token)

    if int(result.serviceStatus.statusCode) == 200:
        session['id'] = result.id
        session['logged_in'] = 1
        if result.role == 'manager':
            session['role'] = 'MANAGER'
        elif result.role == 'editor':
            session['role'] = 'EDITOR'
        elif result.role == 'author':
            session['role'] = 'AUTHOR'
        else:
            session['role'] = 'GUEST'

        output = 'You just logged in as ' + session['role']
        return jsonify({'Authentification succesful! ': output}), 202
    else:
        return jsonify({'Authentification failed! ': "Forbidden"}), 403
    #


@app.route('/api/library/books', methods=['GET'])
def get_all_books():
    global search_attr, search_value

    mycursor = mysql.connection.cursor()

    if request.args.get('title') or request.args.get('genre') or request.args.get('year'):
        if request.args.get('title'):
            search_attr = 'title'
            search_value = '%' + request.args.get('title') + '%'
        if request.args.get('genre'):
            search_attr = 'genre'
            search_value = '%' + request.args.get('genre') + '%'
        if request.args.get('year'):
            search_attr = 'year'
            search_value = '%' + request.args.get('year') + '%'

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

    auth_token = request.headers.get('Authorization')
    cookie = request.headers.get('Cookie')

    if not auth_token or not cookie:
        return jsonify({'Not Authorized ': "Missing cookie or JWT Token"}), 401

    wsdl = 'http://localhost:8080/ws/login.wsdl'
    client = Client(wsdl)

    result = client.service.deleteUserFile(cookie=cookie, token=auth_token)
    print(result)
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host="localhost", port=5005, debug=True)
