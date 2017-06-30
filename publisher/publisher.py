#!/usr/bin/env python
#
# Simple RabbitMQ publisher.
#
# This creates a fanout exchange named "exchange", then publishes a message
# there every 5 seconds.
#
# This is largely boilerplate for the pika Python AMQP client library;
# see https://pika.readthedocs.org/ for details.  This uses a
# callback-oriented style where we perform an operation like "declare
# an AMQP exchange", and the pika library performs it and calls a
# callback when the server has sent back an acknowledgement.  As such,
# there are many short not obviously connected functions.
#
# https://pika.readthedocs.io/en/0.10.0/examples/asynchronous_publisher_example.html
# is a more involved (and robust) example.

# Python 2 syntax options:
from __future__ import (
    # "import foo" is never in the current directory
    absolute_import,
    # / operator is always floating-point, // is integer
    division,
    # "print" is a built-in function, not a statement
    print_function,
)

# If g = partial(f, param), then g(x) calls f(param, x).  We use this
# to push along the AMQP channel object without stuffing it into a
# global or object.
from functools import partial

# Standard library that includes the Unix environment.
import os

# AMQP client library.
import pika


#: Name of the RabbitMQ exchange.
EXCHANGE = 'exchange'

#: AMQP routing key when we send the message.
ROUTING_KEY = 'exchange.example'

#: Delay between sending messages.
DELAY = 5


def main():
    """Main entry point to the program."""

    # Get the location of the AMQP broker (RabbitMQ server) from
    # an environment variable
    amqp_url = os.environ['AMQP_URL']
    print('URL: %s' % (amqp_url,))

    # Actually connect
    parameters = pika.URLParameters(amqp_url)
    connection = pika.SelectConnection(parameters, on_open_callback=on_open)

    # Main loop.  This will run forever, or until we get killed.
    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()


def on_open(connection):
    """Callback when we have connected to the AMQP broker."""
    print('Connected')
    connection.channel(on_channel_open)


def on_channel_open(channel):
    """Callback when we have opened a channel on the connection."""
    print('Have channel')
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout',
                             durable=True,
                             callback=partial(on_exchange, channel))


def on_exchange(channel, frame):
    """Callback when we have successfully declared the exchange."""
    print('Have exchange')
    send_message(channel, 0)


def send_message(channel, i):
    """Send a message to the queue.

    This function also registers itself as a timeout function, so the
    main :mod:`pika` loop will call this function again every 5 seconds.

    """
    msg = 'Message %d' % (i,)
    print(msg)
    channel.basic_publish(EXCHANGE, ROUTING_KEY, msg,
                          pika.BasicProperties(content_type='text/plain',
                                               delivery_mode=2))
    channel.connection.add_timeout(DELAY,
                                   partial(send_message, channel, i+1))


# Python boilerplate to run the main function if this is run as a
# program.  You can 'import publisher' from other Python scripts in
# the same directory to get access to the functions here, or run
# 'pydoc publisher.py' to see the doc strings, and so on, but these
# require this call.
if __name__ == '__main__':
    main()
