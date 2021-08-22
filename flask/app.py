import time

import redis
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'temp',
        'auth_plugin':'mysql_native_password'
    }

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
def index():
    count = get_hit_count()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM log_entry ORDER BY ts DESC LIMIT 20')
    tempdata = [[temp, ts] for (temp, ts) in cursor]
    cursor.execute('SELECT * FROM settings')
    settings = {name: value for (name, value) in cursor}
    cursor.close()
    connection.close()
    return render_template("index.html", count=get_hit_count(), temp=tempdata, data=settings)

@app.route("/settings", methods=['POST', 'GET'])
def settings():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    if request.method == 'POST':
        for k, v in request.form.items():
            print(k, v)
            cursor.execute(f"UPDATE settings SET value = {v} WHERE name = '{k}'")
    cursor.execute('SELECT * FROM settings')
    data = {name: value for (name, value) in cursor}
    cursor.close()
    connection.commit()
    connection.close()
    return render_template("settings.html", count=get_hit_count(), data=data)

@app.route('/history')
def history():
    return render_template("history.html", count=get_hit_count())