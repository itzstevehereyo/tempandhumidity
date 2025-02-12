#Second step: Subscribe to MQTT then insert to MySQL database

import json
import mysql.connector as database
import paho.mqtt.client as mqtt

db = database.connect(
    host = "localhost",
    user = "root",
    password = "Ishy@7853_STeVeyohere",
    database = "tempandhumidity_readings"
)
cursor = db.cursor()

#MQTT Configuration
MQTT_broker = "localhost"
MQTT_port = 1883
MQTT_topics = {
    "readings/temperature": "temperature",
    "readings/humidity": "humidity",
    "readings/clock": "clock",
    "readings/date": "date"
}

tempandhumidity_readings = {"temperature": None, "humidity": None, "clock": None, "date": None}

#Function to be called whenever an MQTT message are received
def MQTTmessage(client, userdata, reading):
    global tempandhumidity_readings
    try:
        data = json.loads(reading.payload.decode("utf-8"))

        key = MQTT_topics[reading.topic]
        tempandhumidity_readings[key] = data[key]

        if all(tempandhumidity_readings.values()):
            sqlQuery = "INSERT INTO readings (temperature, humidity, clock, date) VALUES (%s, %s, %s)"
            values = (
                tempandhumidity_readings["temperature"],
                tempandhumidity_readings["humidity"], 
                tempandhumidity_readings["clock"],
                tempandhumidity_readings["date"]
            )
            cursor.execute(sqlQuery, values)
            db.commit()
            print(f"Inserted into MySQL: {tempandhumidity_readings}")

            tempandhumidity_readings = {"temperature": None, "humidity": None, "clock": None, "date": None}
    except Exception as err:
        print(f"ERROR: {err}")


#Connect to MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = MQTTmessage
mqtt_client.connect(MQTT_broker, MQTT_port, 60)

#Subscribe to MQTT topics
for topic in MQTT_topics.keys():
    mqtt_client.subscribe(topic)


print("Waiting for MQTT messages...")
mqtt_client.loop_forever()



