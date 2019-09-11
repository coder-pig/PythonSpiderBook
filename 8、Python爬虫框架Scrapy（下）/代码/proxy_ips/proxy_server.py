# coding =utf-8
from flask import Flask
from redis import StrictRedis
import random

app = Flask(__name__)


@app.route("/")
def fetch_ip():
    ip_list = list(redis_db.smembers("proxy_ips:proxy_pool"))
    return random.choice(ip_list).decode()


if __name__ == '__main__':
    redis_db = StrictRedis(
        host="127.0.0.1",
        port=6379,
        password="Jay12345",
        db=0
    )
    app.run()

