"""
Simple flask server to act a bridge between the brainwave data and the web app

We include a websocket server to emit events from the server to the client.
"""

from flask import Flask, request, jsonify


# we setup the ws server

from flask_socketio import SocketIO, send, emit

import random

app = Flask(__name__)
import time


app.config['SECRET_KEY'] = 'secret!'

# we setup the websocket server
socketio = SocketIO(app, cors_allowed_origins="*")


# we setup a loop to emit a random coin every 5 seconds


@socketio.on('connect')
def handle_connect():
    if request.sid:
        print(request.sid)
    socketio.start_background_task(target=emit_intention)
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def emit_intention():
    while True:
        time.sleep(5)
        socketio.emit('intention', {'intention': random.choice(['LEFT', 'RIGHT'])})


# we start the loop in a separate thread



coins = [
    {
        'id': '1',
        'name': 'WBTC',
        'price': 10000,
        'volume': 1000,
        'change': 0.5,
        'chain': 'ETH'
    },
    {
        'id': '2',
        'name': 'ETH',
        'price': 1000,
        'volume': 100,
        'change': 0.5,
        'chain': 'ETH'
    },
    {
        'id': '3',
        'name': 'BONK',
        'price': 1,
        'volume': 1000000,
        'change': 0.5,
        'chain': 'SOL'
    }
]

global selected_coin
selected_coin = coins[0]

@app.route('/current_coin', methods=['GET'])
def current_coin():
    return jsonify(selected_coin), 200



# the swipe route takes the coin id and the direction of the swipe
@app.route('/swipe', methods=['POST'])
def swipe():
    global selected_coin
    selected_coin = random.choice(coins)
    coin_id = request.json['coin_id']
    direction = request.json['direction']
    print(coin_id, direction)
    return jsonify({'response': 'OK'}), 200


# we display the transactions

@app.route('/transactions', methods=['GET'])
def transactions():
    return jsonify([
        {"id": "1", "coin": "WBTC", "amount": 100, "price": 10000, "side": "BUY", "status": "FILLED", "tx_hash": "0x1234", "timestamp": "2021-10-10 10:10:10"},
        {"id": "2", "coin": "ETH", "amount": 100, "price": 1000, "side": "SELL", "status": "FILLED", "tx_hash": "0x1234", "timestamp": "2021-10-10 10:10:10"},
    ])

@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    socketio.run(app, debug=True)
