FROM ubuntu:20.04

ENV TZ=US \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential python3 python3-dev python3-pip libpcl-dev \
    libpq-dev postgresql-client gettext g++ gdb make cmake \
    libjpeg8-dev nodejs software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN npm install && npm install -g webpack webpack-cli

EXPOSE 8000 8080

RUN chown webdev:webdev -R .
USER webdev

CMD ["npm", "run", "start"]
