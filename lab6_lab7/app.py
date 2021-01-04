from config import *


@app.route('/api/bookcollection/', methods=['POST'])
def insert_book():
    mysql.connection.cursor()

    username = request.json.get("username")
    password = request.json.get("password")
    paras = {"email": username, "password": password}

    response = requests.post(url="http://0.0.0.0:5002/api/library/login", data=paras)

    if response.status_code == 202:
        role = response.json()['role']

        if role == 'EDITOR':
            editor_id = response.json()['id']
            author_list = request.json['authors']
            title = request.json['title']
            genre = request.json['genre']
            year = request.json['year']

            for a in author_list:
                author_paras = {"fname": a['first_name'], "lname": a['last_name'], "role": 'MANAGER'}
                response = requests.get(url="http://0.0.0.0:5002/api/library/users", data=author_paras)

                author = response.json()
                if author['user'] and response.status_code == 200:
                    book_paras = {"title": title, "author": author['user'][0]['id'], "editor_id": editor_id,
                                  "genre": genre, "year": year}
                    requests.post(url="http://0.0.0.0:5002/api/library/books", data=book_paras)
                else:
                    insert_author_paras = {"fname": a['first_name'], "lname": a['last_name'], "role": 'MANAGER',
                                           "email": a['email'], "password": a['password'], "telephone": a['telephone'],
                                           "req_role": a['req_role']}
                    response_created = requests.post(url="http://0.0.0.0:5002/api/library/users",
                                                     data=insert_author_paras)

                    author_created_id = response_created.json()['created']

                    modify_author_paras = {"user_id": author_created_id, "role": 'MANAGER'}
                    requests.patch(url="http://0.0.0.0:5002/api/library/users/"
                                   + str(author_created_id) + "?requested_role=1",
                                   data=modify_author_paras)

                    book_paras = {"title": title, "author": author_created_id, "editor_id": editor_id,
                                  "genre": genre, "year": year}
                    requests.post(url="http://0.0.0.0:5002/api/library/books/", data=book_paras)

            return jsonify({'Book introduced': title}), 201

        else:
            return jsonify({'You don\'t have the corresponding role': 'Your role is ' + role}), 403
    elif response.status_code == 401:
        return jsonify({'Wrong credentials': response.status_code})


@app.route('/api/bookcollection/<book_id>', methods=['GET'])
def get_book(book_id):
    mysql.connection.cursor()

    response = requests.get(url="http://0.0.0.0:5002/api/library/books/" + str(book_id))
    if response.status_code == 200:
        output = [{'title': response.json()['book'][0]['title'],
                   'author': response.json()['book'][0]['author_name'],
                   'book_genre': response.json()['book'][0]['book_genre'],
                   'book_year': response.json()['book'][0]['book_year']}]

        return jsonify({'Book with id' + book_id + 'is: ': output}), 200
    elif response.status_code == 404:
        return jsonify({'Book with id ' + book_id + ' doesn\'t exist: ': None}), 404
    else:
        return jsonify({'Something went wrong': 'oops'}), 500


@app.route('/api/bookcollection/<book_id>/authors/<author_id>', methods=['GET'])
def get_book_author(book_id, author_id):
    mysql.connection.cursor()

    book_response = requests.get(url="http://0.0.0.0:5002/api/library/books/" + str(book_id))

    if book_response.status_code == 200:
        book_author_id = int(book_response.json()['book'][0]['author_id'])
        if int(author_id) == book_author_id:
            author_response = requests.get(url="http://0.0.0.0:5002/api/library/users/" + str(author_id))
            if author_response.status_code == 200:
                output = [{'name': author_response.json()['user'][0]['name'],
                           'email': author_response.json()['user'][0]['email'],
                           'telephone': author_response.json()['user'][0]['telephone']}]
                return jsonify({'Author with id ' + author_id + ': ': output}), 200
            else:
                return jsonify({'Something went wrong': 'oops'}), 500
        else:
            return jsonify({'Book with id ' + book_id + ' doesn\'t have an author with an id of '
                            + author_id + '.': None}), 404
    elif book_response.status_code == 404:
        return jsonify({'Book with id ' + book_id + ' doesn\'t exist: ': None}), 404
    else:
        return jsonify({'Something went wrong': 'oops'}), 500


if __name__ == '__main__':
    app.run()
