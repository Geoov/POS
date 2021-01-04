from config import *

messages = Blueprint('private_messages_routes', __name__, template_folder="templates")


# noinspection PyBroadException
@messages.route('/api/biblioteca/messages',
                methods=['GET'])  # returneaza toate documentele cu mesajele intre autori <-> editori
def get_messages_documents():  # + search catre / de la implementat
    message = mongo.db.messages
    output = []

    try:
        from_arg = int(request.args.get('from'))
    except:
        from_arg = ""

    try:
        to_arg = int(request.args.get('to'))
    except:
        to_arg = ""

    if from_arg and to_arg:
        for m in message.find({"from": from_arg, "to": to_arg}):
            output.append({'subject': m['subject'], 'text': m['text']})
    else:
        if from_arg:
            for m in message.find({"from": from_arg}):
                output.append(
                    {'id_mesaj': str(m['_id']), 'to_user_id': m['to'], 'subject': m['subject'], 'text': m['text']})
        elif to_arg:
            for m in message.find({"to": to_arg}):
                output.append(
                    {'id_mesaj': str(m['_id']), 'from_user_id:': m['from'], 'subject': m['subject'], 'text': m['text']})
        else:
            for m in message.find():
                output.append({'id_mesaj': str(m['_id']), 'from_user_id:': m['from'], 'to_user_id': m['to'],
                               'subject': m['subject'], 'text': m['text']})

    return jsonify({'messages ': output})


@messages.route('/api/biblioteca/messages/<my_oid>', methods=['GET'])  # returneaza un mesaj dupa _id
def get_one_message(my_oid):
    message = mongo.db.messages
    m = message.find_one({'_id': ObjectId(my_oid)})
    output = []
    if m:
        output.append({'from_user_id:': m['from'], 'to_user_id': m['to'], 'subject': m['subject'], 'text': m['text']})
    else:
        output = "No such id_mesaj"
    return jsonify({'detalii mesaj ': output})


@messages.route('/api/biblioteca/messages', methods=['POST'])  # introduce un mesaj nou
def add_message():
    message = mongo.db.messages

    from_id = request.json['from']
    to_id = request.json['to']
    subject = request.json['subject']
    text = request.json['text']

    message_inserted = message.insert_one({'from': from_id, 'to': to_id, 'subject': subject, 'text': text})
    new_message = message.find_one({'_id': message_inserted.inserted_id})

    output = {'id': new_message['from'], 'to': new_message['to'], 'subject': new_message['subject'],
              'text': new_message['text']}
    return jsonify({'mesaj trimis ': output})


# noinspection PyBroadException
@app.route('/api/biblioteca/users/<my_oid>', methods=['PUT'])  # modifica continutul sau tinta unui mesaj
def update_user(my_oid):
    user = mongo.db.users

    req = request.data
    req_json = req.decode('utf8').replace("'", '"')
    req_json = json.loads(req_json)

    u = user.find_one({'_id': ObjectId(my_oid)})

    if u:
        try:
            u_id = req_json['id']
        except:
            u_id = u['id']

        try:
            favourite_books = req_json['favourite_books']
        except:
            favourite_books = u['favourite_books']

        try:
            wishlist_books = req_json['wishlist']
        except:
            wishlist_books = u['wishlist']

        user.find_one_and_update({'_id': ObjectId(my_oid)},
                                 {'$set':
                                     {
                                         'id': u_id,
                                         'favourite_books': favourite_books,
                                         'wishlist': wishlist_books
                                     }
                                  })
        return jsonify({'user modificat ': req_json})
    else:
        return jsonify({'No such _id ': 0})


@app.route('/api/biblioteca/messages/<my_oid>', methods=['DELETE'])  # sterge un mesaj dupa identificator
def delete_one_message(my_oid):
    global result
    try:
        result = mongo.db.messages.delete_one({'_id': ObjectId(my_oid)})
    finally:
        if result.deleted_count > 0:
            return jsonify({'mesaj sters': result.deleted_count})
        else:
            return jsonify({'mesaj sters': result.deleted_count})
