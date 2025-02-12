from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# Allow requests from any frontend (Change this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="tempandhumidity_readings"
)
cursor = db.cursor(dictionary=True)

@app.get("/latest-readings")
def get_latest_readings():
    cursor.execute("SELECT * FROM readings ORDER BY reading_ID DESC LIMIT 1")
    result = cursor.fetchone()
    return {"status": "success", "data": result} if result else {"status": "error", "message": "No data found"}
