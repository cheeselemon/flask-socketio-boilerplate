import os
import sys
import logging
from config.secrets_manager import SecretsManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Configuration Class
class Config(object):
    
    # TESTING = os.environ.get('TESTING', False)
    # CSRF_ENABLED = True

    # init
    def __init__(self):
        logger.info('[Instance] Config initialized')
        self.debug = os.environ.get('DEBUG', False)
        logger.info(f'[Instance] config.debug = {self.debug}')
        self.secrets_manager = SecretsManager(secret_name='dev/mydoctor-socketio-server')
        self.socket_secret_key = self.secrets_manager.get_value('socket_secret_key')
        logger.info(f'socket_secret_key: {self.socket_secret_key}')


    def redis_endpoint(self):
        if self.debug:
            return 'redis://127.0.0.1:6379/3'
        else:
            try:
                return self.secrets_manager.get_value('redis_endpoint')
            except Exception as e:
                return 'redis://127.0.0.1:6379/3'