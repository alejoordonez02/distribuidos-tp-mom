from typing import Callable

from pika import BlockingConnection, ConnectionParameters

from .middleware import MessageMiddlewareExchange, MessageMiddlewareQueue


class MessageMiddlewareQueueRabbitMQ(MessageMiddlewareQueue):
    def __init__(self, host: str, queue_name: str):
        self.queue_name = queue_name
        self.conn = BlockingConnection(ConnectionParameters(host))
        self.chan = self.conn.channel()
        self.chan.queue_declare(queue=self.queue_name)

    def start_consuming(
        self, on_message_callback: Callable[[bytes, Callable, Callable], None]
    ) -> None:
        def callback(chan, method, properties, body):
            on_message_callback(
                body, lambda: self._ack(chan, method), lambda: self._nack(chan, method)
            )

        self.chan.basic_consume(queue=self.queue_name, on_message_callback=callback)
        self.chan.start_consuming()

    def stop_consuming(self) -> None:
        self.chan.stop_consuming()

    def send(self, message: bytes) -> None:
        self.chan.basic_publish(exchange="", routing_key=self.queue_name, body=message)

    def close(self) -> None:
        self.conn.close()

    def _ack(self, chan, method) -> None:
        chan.basic_ack(delivery_tag=method.delivery_tag)

    def _nack(self, chan, method) -> None:
        chan.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


class MessageMiddlewareExchangeRabbitMQ(MessageMiddlewareExchange):
    def __init__(self, host, exchange_name, routing_keys):
        pass
