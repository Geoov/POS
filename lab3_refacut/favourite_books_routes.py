from config import *

favourites = Blueprint('favourite_books_routes', __name__, template_folder="templates")


# noinspection PyBroadException
@favourites.route('/api/biblioteca/users', methods=['GET'])  # returneaza toate documentele cu cartile preferate /
def get_users_documents():                                   # dorite a fiecarui user sau a unui user ales de utilizator
    user = mongo.db.users
    output = []

    try:
        user_id = int(request.args.get('user'))
    except:
        user_id = ""

    if user_id:
        for u in user.find({"id": user_id}):
            output.append({'favourite_books': u['favourite_books'], 'wishlist': u['wishlist']})
    else:
        for u in user.find():
            output.append({'user_id:': u['id'], 'favourite_books': u['favourite_books'], 'wishlist': u['wishlist']})
    return jsonify({'users ': output})


@favourites.route('/api/biblioteca/users/<my_oid>', methods=['GET'])  # returneaza cartile preferate si/sau dorite ale
def get_one_user(my_oid):                                             # unui user
    user = mongo.db.users
    u = user.find_one({'_id': ObjectId(my_oid)})
    output = []

    if u:
        output.append({'user_id:': u['id'], 'favourite_books': u['favourite_books'], 'wishlist': u['wishlist']})
    else:
        output = "No such _id"
    return jsonify({'detalii_user ': output})


@favourites.route('/api/biblioteca/users', methods=['POST'])  # introduce cartile preferate si/sau dorite ale unui user
def add_user():
    user = mongo.db.users

    u_id = request.json['id']
    favourite_books = request.json['favourite_books']
    wishlist_books = request.json['wishlist']

    user_id = user.insert({'id': u_id, 'favourite_books': favourite_books, 'wishlist': wishlist_books})
    new_user = user.find_one({'_id': user_id})

    output = {'id': new_user['id'], 'favourite_books': new_user['favourite_books'], 'wishlist': new_user['wishlist']}
    return jsonify({'user introdus ': output})


# noinspection PyBroadException
@favourites.route('/api/biblioteca/messages/<my_oid>', methods=['PUT'])  # editeaza / introduce cartile preferate si/sau
def update_message(my_oid):                                              # dorite ale unui user
    message = mongo.db.messages

    req = request.data
    req_json = req.decode('utf8').replace("'", '"')
    req_json = json.loads(req_json)

    m = message.find_one({'_id': ObjectId(my_oid)})

    if m:
        try:
            from_id = req_json['from']
        except:
            from_id = m['from']

        try:
            to_id = req_json['to']
        except:
            to_id = m['to']

        try:
            subject = req_json['subject']
        except:
            subject = m['subject']

        try:
            text = req_json['text']
        except:
            text = m['text']

        message.find_one_and_update({'_id': ObjectId(my_oid)},
                                    {'$set':
                                        {
                                            'from': from_id,
                                            'to': to_id,
                                            'subject': subject,
                                            'text': text
                                        }
                                     })
        return jsonify({'mesaj modificat ': req_json})
    else:
        return jsonify({'No such _id ': 0})


@favourites.route('/api/biblioteca/users/<my_oid>', methods=['DELETE'])  # sterge detaliile despre carti preferate si /
def delete_one_user(my_oid):                                             # sau dorite ale unui user
    global result

    try:
        result = mongo.db.users.delete_one({'_id': ObjectId(my_oid)})
    finally:
        if result.deleted_count > 0:
            return jsonify({'user sters': result.deleted_count})
        else:
            return jsonify({'user sters': result.deleted_count})
