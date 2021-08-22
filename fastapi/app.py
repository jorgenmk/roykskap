import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'temp',
        'auth_plugin':'mysql_native_password'
}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "itsok"}

@app.post("/api/temp")
async def api_temp(temp):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO log_entry (temp, ts) VALUES ({temp}, "{datetime.datetime.now()}")')
    cursor.close()
    connection.commit()
    connection.close()
    return {"message": "postok"}

@app.get("/api/temp")
async def temp_get():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT temp FROM log_entry ORDER BY ts DESC LIMIT 100')
    data = [float(x[0]) for x in cursor]
    cursor.close()
    connection.close()
    return {"message": data}
