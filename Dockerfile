FROM ubuntu:20.04

ENV TZ=US \
    DEBIAN_FRONTEND=noninteractive

EXPOSE 8000
CMD ["./bin/run-prod.sh"]

RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev



RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3 python3-dev python3-pip libpcl-dev \
                                               libpq-dev postgresql-client gettext \
					        g++ gdb make cmake libjpeg8-dev && \
    rm -rf /var/lib/apt/lists/*
#Install libpcl

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q software-properties-common
#RUN add-apt-repository -y ppa:v-launchpad-jochen-sprickerhof-de/pcl # PCL
#RUN apt-get update
# Install pcl
#RUN apt-get install -y libpcl-dev

#RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10
#RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10


# Using PIL or Pillow? You probably want to uncomment next line
# RUN apt-get update && apt-get install -y --no-install-recommends libjpeg8-dev

WORKDIR /app

# Get pip8
#COPY bin/pipstrap.py bin/pipstrap.py
#RUN python bin/pipstrap.py

# First copy requirements.txt and peep so we can take advantage of
# docker caching.
COPY requirements.txt /app/requirements.txt
RUN pip install --require-hashes --no-cache-dir -r requirements.txt

#Copy data into container

COPY . /app
#RUN NEW_RELIC_LICENCE_KEY=001b141e3345317e86299f2337a9c8cd1718d348 NEW_RELIC_APP_NAME=mrfantastic DEBUG=False SECRET_KEY=foo ALLOWED_HOSTS=localhost DATABASE_URL=postgres://localhost/simplex_db DSN=https://762be8db9221413eb6079a4f0e2feb2e:225a22a4224c4fdcb2a8a12c2b6e5a16@app.getsentry.com/66980 ./manage.py collectstatic --noinput -c
RUN chown webdev.webdev -R .
USER webdev
