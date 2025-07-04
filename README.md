# 🅿️ Team1-MagnaLab – Smart Parking System

> This repository contains all of our contributions to the project for the Magna Lab course.
---
## 🚗 Overview

**T1ML** is a smart parking system that integrates hardware and software components to automate the process of vehicle access control, monitoring, and data logging in a physical parking space.

The system uses computer vision, sensors, and a 3D-printed physical gate setup to recognize license plates, control barrier gates, and log parking events in a central database. The project was built using Raspberry Pi, Arduino, and JavaFX as a multidisciplinary solution developed by Team 1 during Magna's Smart Parking System lab.

### 🧠 Key Concept

> A fully functional parking control system that combines:
> - **Computer vision** (license plate recognition)
> - **Hardware actuation** (barriers, servos)
> - **Sensor detection** (presence, movement)
> - **Networked communication** (I2C and DB)
> - **UI for control and monitoring**
---
## 📌 Objectives
- Automate parking entry/exit using license plate recognition (LPR)  
- Control barriers via microcontrollers and sensors  
- Capture and analyze vehicle plates using a Pi camera  
- Log all parking events in a MySQL database  
- Provide modular, maintainable code for each componen  

---
## COMPONENTS
### 🔧 Hardware Components

- **Raspberry Pi 4** – central controller, runs the main Java application
- **Camera Module (PiCam)** – used for license plate recognition (LPR)
- **Arduino Uno** – handles distance and IR sensors, communicates via I2C
- **Ultrasonic + IR sensors** – detect car position and gate entry/exit
- **3D-Printed Barrier System** – servo-controlled gates for car access
- **I2C Communication** – between Arduino and Raspberry Pi


### 💻 Software Components

- **Java 17 + JavaFX** – graphical interface for monitoring system state
- **MySQL** – database for logging vehicle entries/exits and user data
- **OpenCV / Python (optional)** – for license plate recognition
- **Custom I2C Protocol** – for Raspberry ↔ Arduino communication
- **Scene Builder** – used to design JavaFX FXML interfaces
---


## 🔄 System Flow

1. Vehicle approaches the gate.
2. Sensor triggers image capture via PiCam.
3. Raspberry Pi runs recognition (or forwards to external LPR module).
4. If plate is valid → barrier opens automatically.
5. Arduino detects car movement; updates Pi via I2C.
6. Database logs event: plate, timestamp, gate direction.
7. UI updates with session and logs in real-time.
---


## DOCUMENTATION
### **📁 Project Structure**
```
Team1-Magna-Lab/
├── camera_feed.py
├── main.py
├── PlateInfo.md
├── README.md
├── arduino-code/
│   ├── barrier/
│   │   ├── ArduinoCodeForBarrier.ino
│   │   └── lcd-i2c.ino
│   └── serial/
│       ├── a.out
│       ├── testing-serial-usb.c
│       └── testing-serial-usb.py
├── database/
│   ├── add-entry.c
│   ├── create-table.c
│   ├── database-setup.sql
│   └── db.c
├── images/
│   ├── car1.jpg
│   ├── car2.jpeg
│   ├── car3.png
│   ├── ...
│   └── car11.png
├── PiCamImages/
│   ├── Camera stream_screenshot_29.05.2025.png
│   ├── MAI_1.jpg
│   ├── TRICKY_5.jpg
│   └── ...
├── results/
│   ├── pipeline_steps_car1.png
│   ├── pipeline_steps_car2.png
│   └── ...
└── src/
    ├── camera.py
    ├── recognizer.py
    ├── utils.py
    └── validator.py
```

### **[PlateInfo.md](PlateInfo.md)**
Contains detailed documentation about Romanian license plate formats and validation rules:
- Explains the structure and format specifications for different plate types
- Documents the logic behind the validation process
- Provides examples and edge cases for testing
- Serves as a reference guide for understanding the plate validation implementation
---
## CLASS OVERVIEW

### **1. [src/validator.py](src/validator.py)**
Contains the **RomanianLicensePlateValidator** class.
- Validates the format of Romanian license plates based on county codes, numeric part, and letter sequences.
- Supports standard plates for all Romanian counties.
- Handles special plates (military, government) and diplomatic plates.
- Implements comprehensive validation rules:
  - County code validation (all 41 counties + Bucharest)
  - Special prefix validation (A, FA, ALA, MAI)
  - Diplomatic prefix validation (CD, TC, CO)
  - Three-letter sequence validation (rules for I, O, Q, etc.)
  - Number sequence validation for different plate types


### **2. [src/recognizer.py](src/recognizer.py)**
Contains the **NumberPlateRecognizer** class.
- Processes images to identify and extract license plates.
- Implements a complete pipeline: image preprocessing, contour detection, plate extraction, and OCR.
- Provides visualization of all processing steps for debugging.
- Uses pytesseract for Optical Character Recognition of the plate text.

### **3. [src/utils.py](src/utils.py)**
Contains utility functions used across the project.
- `validImageFile`: Validates file extensions for image processing (.jpg, .jpeg, .png).
- Provides common helper functions to support other modules.

### **4. [src/camera.py](src/camera.py)**
Contains the **PiCamera2Stream** class.
- Provides a unified camera interface for different platforms (Raspberry Pi, macOS).
- Handles camera initialization with configurable resolution.
- Manages the video stream and resource cleanup.
- Supports Raspberry Pi Camera Module (using Picamera2) and webcams (using OpenCV).

### **5. [main.py](main.py)**
The central **orchestrator**.
- **Should** capture frames from the camera.
- **Should** recognize potential license plates.
- **Should** validate plate formats.
- **Should** store valid plates and metadata to the server (Firebase).
- **Should** be designed for continuous operation (real-time processing).

---

## 🚀 GETTING STARTED

### **1. Clone the Repository**

```bash
git clone https://github.com/VladTomici14/Team1-Magna-Lab/
cd Team1-Magna-Lab
```

### **2. Dependencies**
- OpenCV (`cv2`) - for image processing and camera interface
- pytesseract - for OCR (Optical Character Recognition)
- numpy - for numerical operations
- imutils - for contour detection
- matplotlib - for visualization
- picamera2 (if running on Raspberry Pi with Bookworm OS)

### **3. Platform Support**
The camera module supports:
- Raspberry Pi (using Picamera2, requires Bookworm OS)
- macOS (using OpenCV webcam interface)
- Support for additional platforms can be implemented as needed

### Results

![Pipeline Steps](results/pipeline_steps_car1.png)
![Pipeline Steps](results/pipeline_steps_car3.png)
![Pipeline Steps](results/pipeline_steps_car7.png)

## 🧠 What Happens After Detection?

1. Plate Validation
The text output from the OCR step is passed through RomanianLicensePlateValidator.
If the plate format is valid (e.g. “B 123 ABC” or “MAI 4567”), the system continues.
If invalid → log error and wait for the next trigger.

2. Database Logging
A new entry is created in the MySQL database with the following fields:  
**Timestamp:** (date and time)  
**Plate string:** (e.g., “B 456 YTR”)  
**Direction:** entry or exit (based on gate position)

3. Barrier Control
A serial signal is sent from the Raspberry Pi to the Arduino.
The Arduino reads the command (e.g., "OPEN"), checks for vehicle presence via sensor, and activates the servo motor.
The gate opens for a limited time or until the car clears the sensor range.

4. Post-Event Logging
A second sensor confirms that the vehicle has passed.
The Arduino sends a signal back to the Pi.
The gate is closed.
The UI (if active) is updated to reflect the latest status.

---
## ELECTRONICS WIRING

This section provides the wiring details for connecting the components to the Arduino board.

![circuit diagram](documentation/circuit.png)

Also, check-out the schematic view of the circuit [here](documentation/Team%201%20-%20Schematic%20View.pdf)!

### **Green LED**
| Component Pin | Arduino Pin |
|---------------|-------------|
| GND           | GND         |
| Pin           | D2          |

### **Red LED**
| Component Pin | Arduino Pin |
|---------------|-------------|
| GND           | GND         |
| Pin           | D3          |

### **Ultrasonic Sensor 1** (HC-SR04)
| Component Pin | Arduino Pin |
|---------------|-------------|
| VCC           | 5V          |
| GND           | GND         |
| Trig          | D11         |
| Echo          | D12         |


### **Ultrasonic Sensor 2** (HC-SR04)
| Component Pin | Arduino Pin |
|---------------|-------------|
| VCC           | 5V          |
| GND           | GND         |
| Trig          | D9          |
| Echo          | D10         |

### **Ultrasonic Sensor 3** (HC-SR04)
| Component Pin | Arduino Pin |
|---------------|-------------|
| VCC           | 5V          |
| GND           | GND         |
| Trig          | D11         |
| Echo          | D12         |


### **Ultrasonic Sensor 4** (HC-SR04)
| Component Pin | Arduino Pin |
|---------------|-------------|
| VCC           | 5V          |
| GND           | GND         |
| Trig          | D9          |
| Echo          | D10         |

### **Servo Motor 1**
| Component Pin | Arduino Pin |
|---------------|-------------|
| VCC           | 5V          |
| GND           | GND         |
| Signal        | D6          |

### **Servo Motor 2**
| Component Pin | Arduino Pin |
|---------------|-------------|
| VCC           | 5V          |
| GND           | GND         |
| Signal        | D6          |

### **LCD Display**
| Component Pin | Arduino Pin |
|---------------|-------------|
| VCC           | 5V          |
| GND           | GND         |
| SDA           | A4          |
| SCL           | A5          |

> ⚠️ Ensure all components share a common GND with the Arduino to avoid inconsistent behavior.


---
## 🧭 EXAMPLE FLOW
🚗 Car arrives → triggers ultrasonic sensor  
📸 PiCam captures image  
🧠 Plate is detected and passed to OCR  
✅ Plate format is validated  
💾 Entry logged to database  
🔓 Arduino opens the gate  
📤 Event confirmed via sensors  
🔒 Gate closes  
🖥️ UI updates / console prints log  