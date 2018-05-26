from flask import Flask
from redis import Redis, RedisError
import os
import socket
import platform

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h1>Hello {name}!</h1>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}<br/>" \
           "<b>Python Version:</b> {pversion}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits,pversion=platform.python_version())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)