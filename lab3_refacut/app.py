from config import *

from private_messages_routes import messages
from favourite_books_routes import favourites

app.register_blueprint(messages)
app.register_blueprint(favourites)


@app.route('/api/biblioteca', methods=['GET'])  # returneaza colectiile
def get_all_collections():
    collections = mongo.db.collection_names()
    output = []
    for c in collections:
        output.append(c)
    return jsonify({'colectii ': output})


if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
