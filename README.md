Docker RabbitMQ Example
=======================

**TL;DR:**
[Install Docker](https://docs.docker.com/engine/installation/), then
run `docker-compose up`.  Control-C will cleanly stop everything.

This is a minimal example that runs [RabbitMQ](http://rabbitmq.com/)
and two small Python messages, all in a single Docker environment.
The `publisher` program publishes a message into RabbitMQ every 5
seconds; the `consumer` program prints every message it recevies to
its stdout.

Once you've brought it all up, you should see the publisher and
consumer printing messages on their stdout.  You can also point a
browser at http://localhost:15672/ (guest/guest) to see the RabbitMQ
management console.  (If you are using a Docker Toolbox or local
Docker Machine environment, try http://192.168.99.100:15672/.)

Another Publisher
-----------------

You can run parts of this environment separately if you'd like.  With
the whole environment running as above, try running the following:

```sh
virtualenv vpy
. vpy/bin/activate
pip install pika

cd publisher
export AMQP_URL=amqp://localhost
./publisher.py
```

The new publisher will start sending its own messages from "Message
0"; both sets of messages will appear on the consumer's output.

In much the same way (continuing to use the same Python virtual
environment) you can run the consumer by hand.  RabbitMQ supports
multiple consumers reading from the same queue and only one of the
consumers will print each message.

Development
-----------

You can run single parts of this; for instance, to run just RabbitMQ
and run it in the background, you can

```sh
docker-compose up -d rabbitmq
```

Now you can run both the publisher and consumer on the console if
you'd like.

As a general development approach, my recommendation would be:

* Develop on the host using
  your [favorite](https://www.gnu.org/software/emacs/) text editor and
  a normally-installed Python, with libraries in a virtual environment

* Write as much non-network code as you can, and use a unit test
  framework like [pytest](https://pytest.org) to write tests for that

* Write simple mock message handlers that batch everything into an
  in-memory queue, and extend your pytest tests to test your message
  handlers.

* Use an environment variable like `AMQP_URL` to indicate the location
  of the broker (if any) and write bigger integration tests that
  `pytest.skip()` themselves if that variable isn't set.

* Only when all of this passes, `docker build` minimal images with
  your application and nothing else installed.  Hand-test the combined
  application.
