import logging

from flask import request

logger = logging.getLogger(__name__)

_namespace = '/sio/doctor'

class DoctorAdmin:
    def __init__(self, socketio, namespace):
        self.socketio = socketio
        self.namespace = namespace if namespace else _namespace

        self.socketio.on_event('connect', self._on_connect, namespace=self.namespace)
        self.socketio.on_event('message', self._handle_message, namespace=self.namespace)

        logger.info(f'DoctorAdmin initialized with namespace : {self.namespace}')
    
    """
    SocketIO Handler Event Functions 
    """
    def _on_connect(self):
        logging.info(f'[{self.namespace}] Client connected - SID : {request.sid}')
        logging.info(f'[{self.namespace}] |-- SID : {request.headers}')
        self.socketio.emit('my response', {'data': 'welcome!'}, namespace=self.namespace)

    def _handle_message(self, message):
        logging.info(f'[{self.namespace}][{request.sid}] received message : {message}')
        self.socketio.emit('my response', {'data': f'{message}'}, namespace=self.namespace)


    """
    REST Handlers 
    """
    def doctor_request(self, doctor_id):
        logging.info(f'[{self.namespace}] received doctor request from doctor_id : {doctor_id}')
        self.socketio.emit('my response', {'data': f'doctor request! doctor_id : {doctor_id}'}, namespace=self.namespace)
        return "ACK"
