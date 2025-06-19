🅿️ Team1-MagnaLab – Smart Parking System

test
This repository contains all of our contributions to the project for the Magna Lab course.
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
🚗 Automate parking entry/exit using license plate recognition (LPR)
🎯 Control barriers via microcontrollers and sensors
📷 Capture and analyze vehicle plates using a Pi camera
💾 Log all parking events in a MySQL database
🔧 Provide modular, maintainable code for each componen

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
## 🚀 Features

- 📸 Automatic license plate detection
- 🛑 Control of entry/exit barriers
- 📍 Real-time vehicle detection via sensors
- 📊 Database logging of events (plate, time, access point)
- 🖥️ JavaFX UI to display active sessions, manual overrides
- 📡 Communication between microcontrollers and UI layer

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

## CLASSES OVERVIEW

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

## GETTNG STARTED

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

## RESULTS

![Pipeline Steps](results/pipeline_steps_car1.png)
![Pipeline Steps](results/pipeline_steps_car3.png)
![Pipeline Steps](results/pipeline_steps_car7.png)
