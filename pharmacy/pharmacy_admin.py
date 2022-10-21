
import logging
from tkinter.font import names

logger = logging.getLogger(__name__)

_namespace = '/sio/pharmacy'

class PharmacyAdmin:
    def __init__(self, socketio, namespace):
        self.socketio = socketio
        self.namespace = namespace if namespace else _namespace

        self.socketio.on_event('connect', self._on_connect, namespace=self.namespace)
        self.socketio.on_event('message', self._handle_message, namespace=self.namespace)

        logger.info(f'PharmacyAdmin initialized with namespace : {self.namespace}')
        
    """
    SocketIO Handler Event Functions 
    """
    def _on_connect(self):
        self.socketio.emit('my response', {'data': 'welcome!'}, namespace=self.namespace)

    def _handle_message(self, message):
        logging.info(f'[{self.namespace}] received message : {message}')
        self.socketio.emit('my response', {'data': 'got it!'}, namespace=self.namespace)
