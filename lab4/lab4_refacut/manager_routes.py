from config import *

manager = Blueprint('manager_routes', __name__, template_folder="templates")


global bit_number
bit_number = 0


# noinspection PyBroadException
@manager.route('/api/library/users', methods=['POST'])
def register_user():
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'MANAGER':
        try:
            fname = request.json['first_name']
            lname = request.json['last_name']
            pss = request.json['password']
            email = request.json['email']
            tel = request.json['telephone']
        except:
            output = 'Wrong paramaters'
            return jsonify({'Register failed! ': output}), 400

        try:
            req_role = request.json['req_role']
        except:
            req_role = 3

        if req_role != 1 and req_role != 2 and req_role != 3 and req_role != 9:
            output = 'No such role'
            return jsonify({'Register failed! ': output}), 400
        else:
            sql_insert_user = 'INSERT INTO users(role_id, first_name, last_name, password, email, telephone, ' \
                              'request_role) VALUES (%s, %s, %s, %s, %s, %s, %s) '
            values_user = ('3', fname, lname, pss, email, tel, req_role)
            mycursor.execute(sql_insert_user, values_user)

            sql_select_last_id = 'SELECT LAST_INSERT_ID()'
            mycursor.execute(sql_select_last_id)

            myresult = mycursor.fetchall()

            mysql.connection.commit()

            output = 'User created with id: ' + str(myresult[0][0])
            return jsonify({'Authentification successful! ': output}), 201
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection DuplicatedCode,PyBroadException
@manager.route('/api/library/users', methods=['GET'])
def get_all_users():
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'MANAGER':
        if request.args.get('requested_role'):
            sql_select_all_users = 'SELECT id, CONCAT(first_name, " ", last_name) name, role_id, email, telephone, ' \
                                   'request_role, password FROM users WHERE request_role = 1 OR request_role = 2;'
        else:
            if request.args.get('name'):
                sql_select_all_users = 'SELECT id, CONCAT(first_name, " ", last_name) name, role_id, email, ' \
                                       'telephone, request_role, password  FROM users WHERE first_name = \'{0}\' ' \
                                       ' OR last_name = \'{0}\''.format(request.args.get('name'))

            elif request.args.get('email'):
                sql_select_all_users = 'SELECT id, CONCAT(first_name, " ", last_name) name, role_id, email, ' \
                                       'telephone, request_role, password  FROM users WHERE email = \'{0}\' ' \
                    .format(request.args.get("email"))
            else:
                sql_select_all_users = 'SELECT id, CONCAT(first_name, " ", last_name) name, role_id, email, ' \
                                       'telephone, request_role, password  FROM users; '

        mycursor.execute(sql_select_all_users)
        myresult = mycursor.fetchall()

        output = []

        for res in myresult:

            if res[2] == 0:
                current_role = 'manager'
            elif res[2] == 1:
                current_role = 'editor'
            elif res[2] == 2:
                current_role = 'author'
            else:
                current_role = 'guest'

            if res[5] == 1:
                requested_role = 'editor'
            elif res[5] == 2:
                requested_role = 'author'
            else:
                requested_role = 'none'

            output.append({'id': res[0], 'name': res[1], 'role': current_role, 'email': res[3], 'telephone': res[4],
                           'requested_role': requested_role, 'password': res[6]})
        return jsonify({'Users are ': output}), 200
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + session['role']
        return jsonify({'Authentification failed! ': output}), 403


# noinspection DuplicatedCode,PyBroadException
@manager.route('/api/library/users/<my_id>', methods=['GET'])
def get_user(my_id):
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == "MANAGER":
        sql_select_user = 'SELECT id, CONCAT(first_name, " ", last_name) name, role_id, email, telephone, ' \
                          'request_role, password FROM users WHERE id = %s; '
        mycursor.execute(sql_select_user, (my_id,))
        myresult = mycursor.fetchall()

        output = []
        if myresult:
            for res in myresult:
                if res[2] == 0:
                    current_role = 'manager'
                elif res[2] == 1:
                    current_role = 'editor'
                elif res[2] == 2:
                    current_role = 'author'
                else:
                    current_role = 'guest'

                if res[5] == 1:
                    requested_role = 'editor'
                elif res[5] == 2:
                    requested_role = 'author'
                else:
                    requested_role = 'none'

                output.append({'id': res[0], 'name': res[1], 'role': current_role, 'email': res[3], 'telephone': res[4],
                               'requested_role': requested_role, 'password': res[6]})
            return jsonify({'User with id ' + my_id + ' is': output}), 200
        else:
            return jsonify({'User with id ' + my_id + ' doesn\'t exit': ''}), 404
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


bin5 = lambda x: ''.join(reversed([str((x >> i) & 1) for i in range(5)]))


# noinspection PyBroadException,PyTypeChecker
@manager.route('/api/library/users/<user_id>', methods=['PATCH'])
def partial_modify_user(user_id):
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'MANAGER':
        sql_select_user = 'SELECT id, request_role FROM users WHERE id = %s;'

        mycursor.execute(sql_select_user, (user_id,))

        myresult = mycursor.fetchall()

        if myresult:
            req = request.data
            try:
                req_json = json.loads(req.decode('utf8').replace("'", '"'))
            except:
                req_json = ''

            global bit_number
            bit_number = 0

            sql_partial_edit_user = 'UPDATE users SET'

            try:
                if req_json['first_name']:

                    sql_partial_edit_user += ' first_name=%s'
                    bit_number += 1
            except:
                sql_partial_edit_user += ''

            try:
                if req_json['last_name']:

                    if bit_number:
                        sql_partial_edit_user += ','
                    sql_partial_edit_user += ' last_name=%s'

                    bit_number += 2
            except:
                sql_partial_edit_user += ''

            try:
                if req_json['email']:
                    if bit_number:
                        sql_partial_edit_user += ','
                    sql_partial_edit_user += ' email=%s'

                    bit_number += 4
            except:
                sql_partial_edit_user += ''

            try:
                if req_json['telephone']:
                    if bit_number:
                        sql_partial_edit_user += ','
                    sql_partial_edit_user += ' telephone=%s'

                    bit_number += 8
            except:
                sql_partial_edit_user += ''

            if request.args.get('requested_role'):
                if myresult[0][1] == 1 or myresult[0][1] == 2:
                    if bit_number:
                        sql_partial_edit_user += ','
                    sql_partial_edit_user += ' role_id = %s, request_role=\'3\''

                    bit_number += 16

            values_list = []

            for i in range(0, len(bin5(bit_number))):
                if bin5(bit_number)[i] != '0':
                    if i == 4:
                        values_list.append(req_json['first_name'])
                    if i == 3:
                        values_list.append(req_json['last_name'])
                    if i == 2:
                        values_list.append(req_json['email'])
                    if i == 1:
                        values_list.append(req_json['telephone'])
                    if i == 0:
                        values_list.append(request.args.get('requested_role'))

            if bit_number == 0:
                output = 'User with id: ' + user_id + ' doesn\'t give any data to be edited'
                return jsonify({'Failed request update!': output}), 400

            sql_partial_edit_user += ' WHERE id = %s'
            values_list.reverse()
            values_list.append(user_id)

            mycursor.execute(sql_partial_edit_user, values_list)

            mysql.connection.commit()

            output = 'User with id: ' + user_id + ' is now updating'
            return jsonify({'Succesful request update!': output}), 200
        else:
            output = 'User with id ' + user_id + ' doesn\'t exit'
            return jsonify({'Failed failed! ': output}), 404
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection PyBroadException
@manager.route('/api/library/users/<user_id>', methods=['PUT'])
def modify_user(user_id):
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'MANAGER':
        req = request.data
        req_json = json.loads(req.decode('utf8').replace("'", '"'))

        sql_edit_user = 'UPDATE users SET role_id=%s, first_name = %s, last_name = %s, password = %s,' \
                        ' email= %s, telephone=%s, request_role=%s WHERE id = %s'

        sql_insert_user = 'INSERT INTO users(id, role_id, first_name, last_name, password, email, telephone, ' \
                          'request_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '

        try:
            req_role = request.json['req_role']
        except:
            req_role = 3

        try:
            mycursor.execute(sql_insert_user, (user_id, 3, req_json['first_name'], req_json['last_name'],
                                               req_json['password'], req_json['email'], req_json['telephone'],
                                               req_role))

            mysql.connection.commit()

            output = 'User created with id: ' + user_id
            return jsonify({'Authentification successful! ': output}), 201

        except:
            mycursor.execute(sql_edit_user, (3, req_json['first_name'], req_json['last_name'],
                                             req_json['password'], req_json['email'], req_json['telephone'],
                                             req_role, user_id))

            mysql.connection.commit()

            output = 'User with id: ' + user_id + ' is now updated'
            return jsonify({'Succesful update!': output}), 200  # 204 e standard NO CONTENT da pentru afisare mere

    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403


# noinspection PyBroadException
@manager.route('/api/library/users/<my_id>', methods=['DELETE'])
def delete_user(my_id):
    mycursor = mysql.connection.cursor()

    try:
        is_logged = session['logged_in']
    except:
        is_logged = 0

    if is_logged == 0:
        session['role'] = 'GUEST'

    role = session['role']

    if role == 'MANAGER':
        sql_delete_user = 'DELETE FROM users WHERE id = %s'
        value_delete_user = int(my_id)
        res = mycursor.execute(sql_delete_user, (value_delete_user,))

        mysql.connection.commit()

        if res:
            output = 'User with id ' + my_id + ' deleted'
            return jsonify({'Delete successful! ': output}), 204
        else:
            output = 'User with id ' + my_id + ' doesn\'t exit'
            return jsonify({'Delete failed! ': output}), 404
    else:
        output = 'You don\'t have the coressponding role; Your role is ' + role
        return jsonify({'Authentification failed! ': output}), 403
