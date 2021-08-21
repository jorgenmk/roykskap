import datetime

from fastapi import FastAPI
import mysql.connector

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "itsok"}

@app.post("/api/temp")
async def api_temp(temp):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'temp',
        'auth_plugin':'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO log_entry (temp, ts) VALUES ({temp}, "{datetime.datetime.now()}")')
    cursor.close()
    connection.commit()
    connection.close()
    return {"message": "Hello posted"}