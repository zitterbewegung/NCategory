#!/bin/sh

./bin/run-common.sh
./manage.py runserver 0.0.0.0:8000
./node_modules/.bin/webpack --config webpack.config.js --watch
