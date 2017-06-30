# Dockerfile for the publisher application.
#
# 'docker-compose build' from the parent directory will build this.
# 'docker-compose up' will too, if it needs to be.
#
# To build this by hand, cd into the "publisher" directory and run
# 'docker build -t publisher .', and then you can manually run
# 'docker run --rm -e AMQP_URL=... publisher' to run it.

# This is based on the Python 2.7 Alpine Linux image.  See
# https://hub.docker.com/_/python/ for details on this image.
FROM python:2.7-alpine

# Our requirements are minimal, but it's good practice to install them
# first.  Put things that change less often towards the top of the
# Dockerfile.  Then if you need to rebuild the images, Docker will
# start running partway through the Dockerfile and skip over the steps
# where nothing's changed.
RUN pip install pika

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1

# Actually install the application
WORKDIR /usr/src/app
# It's only a single file.  It has to be in the same directory as the
# Dockerfile, or a subdirectory, but not a parent or sibling.
COPY publisher.py .

# When you just 'docker run publisher' with no command afterwards,
# default to this:
CMD ["python", "/usr/src/app/publisher.py"]
