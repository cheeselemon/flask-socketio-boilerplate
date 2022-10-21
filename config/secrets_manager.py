# sys level imports 
import base64
import json
import logging

# dependency imports 
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class SecretsManager:
    service_name = 'secretsmanager'
    data = None

    def __init__(self, secret_name, region_name='ap-northeast-2'):
        logger.info('[Instance] SecretsManager initialized')
        session = boto3.session.Session()
        self.secret_name = secret_name
        self.region_name = region_name
        self.client = session.client(
            service_name=self.service_name,
            region_name=self.region_name
        )

    @staticmethod
    def _to_dict(data):
        """_to_dict(data: str) -> dict"""
        return json.loads(data)

    @staticmethod
    def _to_binary(data):
        """_to_binary(data: str) -> bytes"""
        return base64.b64decode(data) if data else None

    def request_error_handler(self, error):
        """SecretsRequester error handler.

        Args:
            error (Exception): Any error to handle properly.

        """
        if error.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise error
        if error.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise error
        if error.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise error
        if error.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise error
        if error.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise error
        if error.response['Error']['Code'] == 'UnrecognizedClientException':
            # Wrong token provided.
            # Check your `.env`, or system aws configuration or else.
            raise error
        if error.response['Error']['Code'] == 'ExpiredTokenException':
            # Expired session token provided.
            # Check your aws mfa configuration.
            raise error

        logger.debug(error)

    @property
    def response(self):
        """response -> (dict, bytes, None)"""
        logger.info("Sending requests to AWS Secrets Manager '%s'", self.secret_name)

        try:
            secret_response = self.client.get_secret_value(SecretId=self.secret_name)
            if 'SecretString' in secret_response:
                # common key-value data
                data = secret_response['SecretString']
                try:
                    # 먼저 key/value 형태로 변환을 시도하고, 실패하면 string 형태로 돌려줍니다.
                    return self._to_dict(data)
                except json.decoder.JSONDecodeError:
                    return secret_response['SecretString']

            if 'SecretBinary' in secret_response:
                # binary data`
                data = secret_response['SecretBinary']
                return self._to_binary(data)

        except ClientError as e:
            return self.request_error_handler(error=e)
        return None

    """
        key/value pair의 값을 읽어옵니다.
    """
    def get_value(self, key, default=None):
        if not self.data:
            self.data = self.response
        return self.data.get(key, default)

    """
        AWS의 Secrets Manager 에서 key/value pair가 아닌 string 데이터를 읽어오는데 사용합니다. 
    """
    def get_plain_data(self):
        if not self.data:
            self.data = self.response
        return self.data
