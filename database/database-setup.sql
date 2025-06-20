-- Database creation (run once)
CREATE DATABASE IF NOT EXISTS team1_parking;
USE team1_parking;

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL UNIQUE,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_authorized BOOLEAN DEFAULT TRUE
);