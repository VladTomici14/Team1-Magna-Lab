-- Database creation (run once)
CREATE DATABASE IF NOT EXISTS team1_parking;
USE team1_parking;

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL UNIQUE,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_authorized BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS parking_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    event_type ENUM('ENTRY', 'EXIT') NOT NULL,
    event_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    anpr_confidence DECIMAL(5,2),
    image_path VARCHAR(255),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);

CREATE TABLE IF NOT EXISTS parking_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL UNIQUE,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME,
    parking_duration INT,
    status ENUM('IN', 'OUT') NOT NULL DEFAULT 'IN',
    entry_event_id INT,
    exit_event_id INT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (entry_event_id) REFERENCES parking_events(event_id),
    FOREIGN KEY (exit_event_id) REFERENCES parking_events(event_id),
    INDEX idx_active_sessions (status, vehicle_id)
);

CREATE TABLE IF NOT EXISTS system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    log_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level ENUM('INFO', 'WARNING', 'ERROR') NOT NULL,
    source VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    related_plate VARCHAR(20)
);