# sys imports 
import os
import re
import sys
import logging


# dependency imports 
from flask import Flask
from flask_socketio import SocketIO
# import eventlet; eventlet.monkey_patch(socket=False)
import eventlet; eventlet.monkey_patch()

# app level imports 
from config.config import Config
from doctor.doctor_admin import DoctorAdmin
from pharmacy.pharmacy_admin import PharmacyAdmin


config = Config()


# Initialize App 
app = Flask(__name__)
app.debug = config.debug
app.config['SECRET_KEY'] = config.socket_secret_key

# Create socketio 
# socketio = SocketIO(app, message_queue='redis://')
socketio = SocketIO(app, message_queue=config.redis_endpoint(), async_mode='eventlet', cors_allowed_origins='*', path='sio')

# Initialize socketio namespace handlers 
doctor_admin = DoctorAdmin(socketio, namespace='/doctor')
pharmacy_admin = PharmacyAdmin(socketio, namespace='/pharmacy')

# Define REST Input 
app.add_url_rule("/doctor/<int:doctor_id>/request", view_func=doctor_admin.doctor_request)  

@app.route('/trigger')
def trigger():
    socketio.emit('my response', {'data': 'triggered!'})
    return 'triggered!'

if __name__ == '__main__':
    # Run socketio
    logging.info('[Init] socketio up and running')
    socketio.run(app, port=8000, debug=config.debug)
