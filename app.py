#! .venv_linux/bin/python3
from models.validator import OrderValidate, FilterValidate
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
import uvicorn
import sqlite3
import csv


DB_PATH = "database/database.db"


app = FastAPI()


# Homepage
@app.get("/")
async def root():
    return {"message": "Hello, Mains Lab!"}


# Endpoint for upload csv-data
@app.post("/upload")
async def upload():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                    (client_name TEXT NOT NULL,
                    client_org TEXT NOT NULL,
                    num INTEGER NOT NULL,
                    total NOT NULL,
                    date TEXT NOT NULL,
                    service TEXT NOT NULL,
                    UNIQUE (client_name, client_org, num));''')

        # Reading csv data
        with open('data/bills.csv', 'r', encoding="utf-8") as file:
            data = csv.DictReader(file)
            data_list = []
            for row in data:
                try:
                    data_list.append((row['client_name'],
                                      row['client_org'],
                                      int(row['№'].replace(",", ".")),
                                      float(row['sum'].replace(",", ".")),
                                      row['date'],
                                      row['service']))

                except Exception as _ex:
                    print(_ex)

        response = []
        # Validate and export to table valid data
        for row in data_list:
            row_json = jsonable_encoder(zip(('client_name', 'client_org', 'num', 'total', 'date', 'service'), row))
            try:
                OrderValidate.parse_obj(row_json)
                cursor.execute('''INSERT or IGNORE INTO clients (
                                client_name,
                                client_org,
                                num,
                                total,
                                date,
                                service)
                                VALUES (?, ?, ?, ?, ?, ?);''', row)
                response.append(row)
            except ValidationError as _ex:
                print(_ex.json())
        return response

    except sqlite3.Error as _ex:
        print(_ex)

    finally:
        if connection:
            connection.commit()
            connection.close()


# Endpoint for get info about orders fith filers
@app.get("/getorderlist")
async def getorderlist(filter: str = None, value: str = None):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        if filter == None or value == None:
            data = cursor.execute("SELECT * FROM clients").fetchall()
        else:
            try:
                FilterValidate.parse_obj({"filter": filter})
                data = cursor.execute(f"SELECT * FROM clients WHERE {filter} = ?", (value,)).fetchall()
            except ValidationError as _ex:
                print(_ex.json())

        response = jsonable_encoder(data)
        return response

    except sqlite3.Error as _ex:
        print(_ex)

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, host="127.0.0.1", reload=True)
