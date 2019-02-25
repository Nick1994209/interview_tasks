import os

MAX_CONNECTIONS_BY_FETCHER = 10
CONNECTION_TIMOUT = 30

BASE_PROXY_HEADERS = {'Content-Type', 'Content-Length', 'Location'}

APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
APP_PORT = int(os.environ.get('APP_PORT', '8080'))
