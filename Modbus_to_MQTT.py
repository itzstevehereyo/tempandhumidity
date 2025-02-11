#First step: Modbus RTU data to MQTT in JSON format

import json
import time
import paho.mqtt.client as mqtt
from pymodbus.client import ModbusSerialClient as ModbusClient

#registers to read
Starting_address = 0

#setting up MQTT
MQTT_broker = "localhost"
MQTT_port = 1883
MQTT_topic_temp = "readings/temperature"
MQTT_topic_humid = "readings/humidity"
MQTT_topic_clock = "readings/clock"
MQTT_topic_date = "readings/date"

#connect to sensor
client = ModbusClient(
    port = "COM5",
    baudrate = 4800,
    parity = "N",
    stopbits = 1,
    bytesize = 8,
    timeout = 1
)

#connect to MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_broker, MQTT_port, 60)

if not client.connect():
    print("CONNECTION ERROR: Failed to connect with the Modbus RTU device.")
    exit()

try: 
    while True:
        ReadModbusData = client.read_holding_registers(address=Starting_address, count=2, slave=1)

        if ReadModbusData.isError():
            print("DATA READING ERROR: Failed to read Modbus data.")
        else:
            humidity = ReadModbusData.registers[0] / 10
            temperature = ReadModbusData.registers[1] / 10
            clock = time.strftime("%H:%M:%S")
            date = time.strftime("%d-%m-%Y ")

            temp_JSON = json.dumps({"temperature": temperature})
            humid_JSON = json.dumps({"humidity": humidity})
            clock_JSON = json.dumps({"time": clock})
            date_JSON = json.dumps({"date": date})

            mqtt_client.publish(MQTT_topic_temp, temp_JSON)
            mqtt_client.publish(MQTT_topic_humid, humid_JSON)
            mqtt_client.publish(MQTT_topic_clock, clock_JSON)
            mqtt_client.publish(MQTT_topic_date, date_JSON)

            print(f"Published: {temp_JSON}, {humid_JSON}, {clock_JSON}{date_JSON}")

        time.sleep(1)
except KeyboardInterrupt:
    print("Data reading stopped.")
finally:
    client.close()
    mqtt_client.disconnect()
