import pika
from pika.spec import PERSISTENT_DELIVERY_MODE

from app.exceptions import RabbitConnectionClosedError
from config import Config


class RabbitContext:

    def __init__(self, **kwargs):
        self._host = kwargs.get('host') or Config.RABBIT_HOST
        self._port = kwargs.get('port') or Config.RABBIT_PORT
        self._vhost = kwargs.get('vhost') or Config.RABBIT_VIRTUALHOST
        self._user = kwargs.get('user') or Config.RABBIT_USERNAME
        self._password = kwargs.get('password') or Config.RABBIT_PASSWORD
        self.queue_name = kwargs.get('queue_name') or Config.RABBIT_QUEUE
        self._exchange = Config.RABBIT_EXCHANGE

    def __enter__(self):
        self.open_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    @property
    def channel(self):
        return self._channel

    def open_connection(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(self._host,
                                      self._port,
                                      self._vhost,
                                      pika.PlainCredentials(self._user, self._password)))

        self._channel = self._connection.channel()

        return self._connection

    def close_connection(self):
        self._connection.close()
        del self._channel
        del self._connection

    def publish_message(self, message: str, content_type: str):
        if not self._connection.is_open:
            raise RabbitConnectionClosedError

        self._channel.basic_publish(exchange='action-outbound-exchange',
                                    routing_key='Action.Printer.binding',
                                    body=message,
                                    properties=pika.BasicProperties(content_type=content_type))
