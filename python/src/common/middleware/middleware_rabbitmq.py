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
        pass

    def stop_consuming(self) -> None:
        pass

    def send(self, message: bytes) -> None:
        pass

    def close(self) -> None:
        self.conn.close()


class MessageMiddlewareExchangeRabbitMQ(MessageMiddlewareExchange):
    def __init__(self, host, exchange_name, routing_keys):
        pass
