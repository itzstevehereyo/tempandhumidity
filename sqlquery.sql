CREATE DATABASE tempandhum;
USE tempandhum;

CREATE TABLE sensor_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT
);
    
SELECT * FROM sensor_readings;
DROP TABLE sensor_readings;
