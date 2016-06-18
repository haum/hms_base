import logging
import json

import pika


def get_logger():
    return logging.getLogger(__name__)


class Client:
    """Overlay for easy microservices communication."""

    def __init__(self, name, exchange, routing_keys, enable_ping=True):
        """Initialize the client with connection settings.

        Args:
            name; name of the client
            exchange: name of the exchange to connect to
            routing_keys: list of routing keys to listen to
            enable_ping: enable answering to ping requests

        By default, the 'ping' routing key will be added in order to enable
        response to ping requests expect specified otherwise.

        """
        self.name = name
        self.exchange = exchange
        self.routing_keys = routing_keys
        self.listeners = []

        if enable_ping:
            self.listeners.append(self._handle_ping)
            if 'ping' not in self.routing_keys:
                self.routing_keys.append('ping')

        self.channel = None
        self.conn = None
        self.queue_name = None

    def connect(self, host='localhost'):
        """Connect to the server and set everything up.

        Args:
            host: hostname to connect to

        """

        # Connect

        get_logger().info("Connecting to RabbitMQ server...")

        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.conn.channel()

        # Exchanger

        get_logger().info("Declaring direct exchanger {}...".format(
            self.exchange))

        self.channel.exchange_declare(exchange=self.exchange, type='direct')

        # Create queue

        get_logger().info("Creating RabbitMQ queue...")
        result = self.channel.queue_declare(exclusive=True)

        self.queue_name = result.method.queue

        # Binding

        for routing_key in self.routing_keys:
            get_logger().info(
                "Binding queue to exchanger {} with routing key {}...".format(
                    self.exchange, routing_key))

            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key=routing_key)

        # Callback

        get_logger().info("Binding callback...")
        self.channel.basic_consume(
            self._callback, queue=self.queue_name, no_ack=True)

    def publish(self, routing_key, dct):
        """Send a dict with internal routing key to the exchange."""
        get_logger().info("Publishing message {} on routing key "
                          "{}...".format(dct, routing_key))

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=json.dumps(dct)
        )

    def start_consuming(self):
        """Start the infinite blocking consume process."""
        get_logger().info("Starting passive consuming...")
        self.channel.start_consuming()

    def stop_consuming(self):
        """Stop the consume process."""
        get_logger().info("Stopping passive consuming...")
        self.channel.stop_consuming()

    def disconnect(self):
        """Disconnect from the RabbitMQ server."""
        get_logger().info("Disconnecting from RabbitMQ server...")
        self.conn.close()

    def _callback(self, *args):
        """Internal method that will be called when receiving message."""

        get_logger().info("Message received! Calling listeners...")

        for li in self.listeners:
            li(*args)

    def _handle_ping(self, ch, method, properties, body):

        if method.routing_key == 'ping':
            payload = json.loads(body.decode('utf-8'))

            if payload['type'] == 'request':
                resp = {
                    'type': 'answer',
                    'name': self.name,
                    'source': payload
                }

                self.publish('ping', resp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    c = Client('test', 'haum', ['test'])
    c.connect()

    try:
        c.start_consuming()
    except KeyboardInterrupt:
        get_logger().critical("Got a KeyboardInterrupt")
        c.stop_consuming()
        c.disconnect()
