import time

import redis
from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'temp',
        'auth_plugin':'mysql_native_password'
    }
    count = get_hit_count()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM log_entry ORDER BY ts ASC LIMIT 20')
    data = [[temp, ts] for (temp, ts) in cursor]
    cursor.close()
    connection.close()
    return render_template("base.html", count=count, temp=data, title="Title", header="Header")


