from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'Store №1',
        'items': [
            {
                'name': 'chair',
                'price': 999
            },
            {
                'name': 'mirror',
                'price': 3500
            },
            {
                'name': 'bed',
                'price': 25000
            }
        ] 
    },
    {
        'name': 'Store №2',
        'items': [
            {
                'name': 'chair',
                'price': 2000
            },
            {
                'name': 'mirror',
                'price': 5500
            },
            {
                'name': 'bed',
                'price': 33000
            }
        ] 
    }
]


# POST /store -> name
@app.route('/store', methods=['POST'])
def create_store():
    data = request.get_json()
    new_store = {
        'name': data['name'],
        'items': []
    }
    stores.append(new_store)
    return new_store


# GET /store/<name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


# GET /store
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<name>/item -> name, price
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    data = request.get_json()
    new_item = {
        'name': data['name'],
        'price': data['price']
    }
    for store in stores:
        if store['name'] == name:
            store['items'].append(new_item)
            return new_item
    return jsonify({'message': 'store not found'})


# GET /store/<name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({'message': 'store not found'})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4444)
