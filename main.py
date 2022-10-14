from flask import Flask
from flask_socketio import SocketIO, emit

import sys
import logging

# configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Initialize App 
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'

# Create socketio 
socketio = SocketIO(app)

# Handle messages 
@socketio.on('message')
def handle_message(data):
    logging.info('received message: ' + data)
    emit("default", "default response")
    emit('default', {'data': 'namespace'}, namespace='/test')

# Handle on connect
@socketio.on('connect')
def test_connect(auth):
    logging.info('Client connected')
    emit('default', {'data': 'Connected'})

# handle disconnect 
@socketio.on('disconnect')
def test_disconnect():
    logging.info('Client disconnected')

if __name__ == '__main__':
    # Run socketio
    logging.info('initializing socketio')
    socketio.run(app, debug=True)
