from fastapi import FastAPI
import mysql.connector

app = FastAPI()

#MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="tempandhumidity_readings"
)
cursor = db.cursor(dictionary=True)

#Get latest sensor readings
@app.get("/latest-readings")

def getLatestReadings():
    try:
        cursor.execute("SELECT * FROM readings ORDER BY reading_ID DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            return {"status": "success","data": result}
        else:
            return {"status": "error", "message": "No data found"}
    except Exception as err:
        return {"status": "error", "message":str(err)}
