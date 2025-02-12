# Temperature and Humidity Sensor Monitoring

This repository contains the publication of Modbus RTU data obtained from a temperature and humidity sensor using the Message Queueing Telemetry Transport (MQTT) protocol. The data are formatted in JSON. The MQTT messages are then subscribed to using a separate Python script, and then the subscribed data are stored inside MySQL. An API is created where it will pull the latest sensor readings from the MySQL database.

A web dashboard is created to monitor the temperature and humidity, visualized in a user interface. When the temperature is too high, the website will show an alert through an unremovable window and will be dismissed once the temperature readings are back to normal.
