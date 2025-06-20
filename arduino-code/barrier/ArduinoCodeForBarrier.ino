#include <Servo.h>
#include <LiquidCrystal_I2C.h>

// ----- Pin Definitions -----
#define ENTRY_TRIG 11
#define ENTRY_ECHO 12
#define ENTRY_SAFE_TRIG 3
#define ENTRY_SAFE_ECHO 4

#define EXIT_TRIG 9
#define EXIT_ECHO 10
#define EXIT_SAFE_TRIG 7
#define EXIT_SAFE_ECHO 8

#define SERVO_ENTRY_PIN 5
#define SERVO_EXIT_PIN 6

#define OPEN_ANGLE 75
#define CLOSED_ANGLE 0
#define STEP_DELAY 15
#define BUFFER_SIZE 5
#define DETECTION_DISTANCE 15  // cm - distance to panels
#define SENSOR_UPDATE_INTERVAL 100  // ms
#define SIGNAL_SEND_INTERVAL 1000  // ms for car detection signals

// ----- LCD -----
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ----- Barrier Struct -----
struct Barrier {
  int trigPin;
  int echoPin;
  int safeTrigPin;
  int safeEchoPin;
  Servo* servo;

  int bufferBefore[BUFFER_SIZE] = {0};
  int bufferAfter[BUFFER_SIZE] = {0};
  int indexBefore = 0;
  int indexAfter = 0;

  bool carBefore = false;
  bool carAfter = false;
  bool lastCarBefore = false;
  bool lastCarAfter = false;

  bool barrierOpened = false;
  bool opening = false;
  bool closing = false;
  int angle = CLOSED_ANGLE;
  unsigned long lastMoveTime = 0;

  // Entry barrier needs permission, exit barrier opens automatically
  bool waitingForPermission = false;
  bool hasPermission = false;

  Barrier(int trig, int echo, int safeTrig, int safeEcho, Servo* s)
    : trigPin(trig), echoPin(echo), safeTrigPin(safeTrig), safeEchoPin(safeEcho), servo(s) {}
};

// ----- Servo Instances -----
Servo entryServo, exitServo;

// ----- Barrier Instances -----
Barrier entry(ENTRY_TRIG, ENTRY_ECHO, ENTRY_SAFE_TRIG, ENTRY_SAFE_ECHO, &entryServo);
Barrier exitBarrier(EXIT_TRIG, EXIT_ECHO, EXIT_SAFE_TRIG, EXIT_SAFE_ECHO, &exitServo);

// ----- Timing Variables -----
unsigned long lastSensorUpdate = 0;
unsigned long lastEntrySignal = 0;

// ----- Utility Functions -----
long readDistanceCM(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  long duration = pulseIn(echo, HIGH, 30000);  // 30ms timeout
  if (duration == 0) return 999;  // Return large value for timeout

  return (duration * 0.0343) / 2.0;
}

bool isCarDetected(int trig, int echo) {
  long distance = readDistanceCM(trig, echo);
  // Car is present when distance is less than 15cm (panel distance)
  // Valid reading should be > 0 and < 15cm
  return (distance > 0 && distance < DETECTION_DISTANCE);
}

void updateCarPresence(Barrier &b) {
  // Update "before" sensor (car approaching)
  int carDetectedBefore = isCarDetected(b.trigPin, b.echoPin) ? 1 : 0;
  b.bufferBefore[b.indexBefore] = carDetectedBefore;
  b.indexBefore = (b.indexBefore + 1) % BUFFER_SIZE;

  // Update "after" sensor (car passed through)
  int carDetectedAfter = isCarDetected(b.safeTrigPin, b.safeEchoPin) ? 1 : 0;
  b.bufferAfter[b.indexAfter] = carDetectedAfter;
  b.indexAfter = (b.indexAfter + 1) % BUFFER_SIZE;

  // Calculate presence based on buffer majority
  int sumBefore = 0, sumAfter = 0;
  for (int i = 0; i < BUFFER_SIZE; i++) {
    sumBefore += b.bufferBefore[i];
    sumAfter += b.bufferAfter[i];
  }

  b.lastCarBefore = b.carBefore;
  b.lastCarAfter = b.carAfter;

  b.carBefore = (sumBefore >= BUFFER_SIZE - 1);  // 4 out of 5 readings
  b.carAfter = (sumAfter >= BUFFER_SIZE - 1);
}

void moveBarrier(Barrier &b) {
  unsigned long now = millis();

  if ((b.opening || b.closing) && now - b.lastMoveTime >= STEP_DELAY) {
    b.lastMoveTime = now;

    if (b.opening && b.angle < OPEN_ANGLE) {
      b.angle+=5;
      b.servo->write(b.angle);
    } else if (b.opening && b.angle >= OPEN_ANGLE) {
      b.opening = false;
      b.barrierOpened = true;
      Serial.println("BARRIER_OPENED");
    }

    if (b.closing && b.angle > CLOSED_ANGLE) {
      b.angle-=5;
      b.servo->write(b.angle);
    } else if (b.closing && b.angle <= CLOSED_ANGLE) {
      b.closing = false;
      b.barrierOpened = false;
      Serial.println("BARRIER_CLOSED");
    }
  }
}

void handleEntryBarrier() {
  updateCarPresence(entry);

  // Car just arrived at entry barrier
  if (entry.carBefore && !entry.lastCarBefore && !entry.waitingForPermission && !entry.barrierOpened) {
    entry.waitingForPermission = true;
    Serial.println("CAR_DETECTED_ENTRY");
    updateLCD("Car Detected", "Checking Plate...");
  }

  // Open barrier when permission is granted
  if (entry.waitingForPermission && entry.hasPermission && entry.carBefore && !entry.barrierOpened) {
    entry.opening = true;
    entry.closing = false;
    entry.waitingForPermission = false;
    entry.hasPermission = false;
    Serial.println("ENTRY_BARRIER_OPENING");
    updateLCD("Access Granted", "Barrier Opening");
  }

  // Close barrier when car has passed
  if (entry.barrierOpened && entry.lastCarAfter && !entry.carAfter) {
    entry.closing = true;
    entry.opening = false;
    Serial.println("ENTRY_BARRIER_CLOSING");
    updateLCD("Car Passed", "Barrier Closing");
  }

  // Reset if car leaves without permission
  if (entry.waitingForPermission && !entry.carBefore && entry.lastCarBefore) {
    entry.waitingForPermission = false;
    Serial.println("CAR_LEFT_ENTRY");
    updateLCD("Ready", "");
  }

  moveBarrier(entry);
}

void handleExitBarrier() {
  updateCarPresence(exitBarrier);

  // Car detected at exit - open automatically
  if (exitBarrier.carBefore && !exitBarrier.lastCarBefore && !exitBarrier.barrierOpened) {
    exitBarrier.opening = true;
    exitBarrier.closing = false;
    Serial.println("CAR_DETECTED_EXIT");
    Serial.println("EXIT_BARRIER_OPENING");
    updateLCD("Car Exiting", "Barrier Opening");
  }

  // Close barrier when car has passed
  if (exitBarrier.barrierOpened && exitBarrier.lastCarAfter && !exitBarrier.carAfter) {
    exitBarrier.closing = true;
    exitBarrier.opening = false;
    Serial.println("EXIT_BARRIER_CLOSING");
    updateLCD("Car Exited", "Barrier Closing");
  }

  moveBarrier(exitBarrier);
}

void updateLCD(String line1, String line2) {
  static String lastLine1 = "";
  static String lastLine2 = "";

  if (line1 != lastLine1 || line2 != lastLine2) {
    lcd.clear();

    // Center text on LCD
    int pos1 = (16 - line1.length()) / 2;
    int pos2 = (16 - line2.length()) / 2;

    lcd.setCursor(max(0, pos1), 0);
    lcd.print(line1);

    if (line2.length() > 0) {
      lcd.setCursor(max(0, pos2), 1);
      lcd.print(line2);
    }

    lastLine1 = line1;
    lastLine2 = line2;
  }
}

void handleSerialCommands() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toLowerCase();

    Serial.print("RECEIVED_COMMAND: ");
    Serial.println(command);

    if (command == "plate_valid" || command == "open_entry") {
      if (entry.waitingForPermission) {
        entry.hasPermission = true;
        Serial.println("ENTRY_PERMISSION_GRANTED");
      } else {
        Serial.println("NO_CAR_WAITING_ENTRY");
      }
    }
    else if (command == "plate_invalid") {
      if (entry.waitingForPermission) {
        entry.waitingForPermission = false;
        Serial.println("ENTRY_PERMISSION_DENIED");
        updateLCD("Access Denied", "Invalid Plate");
        delay(2000);
        updateLCD("Ready", "");
      }
    }
    else if (command == "status") {
      Serial.println("=== SYSTEM STATUS ===");
      Serial.print("Entry - Car Before: ");
      Serial.print(entry.carBefore ? "YES" : "NO");
      Serial.print(", Car After: ");
      Serial.print(entry.carAfter ? "YES" : "NO");
      Serial.print(", Barrier: ");
      Serial.println(entry.barrierOpened ? "OPEN" : "CLOSED");

      Serial.print("Exit - Car Before: ");
      Serial.print(exitBarrier.carBefore ? "YES" : "NO");
      Serial.print(", Car After: ");
      Serial.print(exitBarrier.carAfter ? "YES" : "NO");
      Serial.print(", Barrier: ");
      Serial.println(exitBarrier.barrierOpened ? "OPEN" : "CLOSED");
      Serial.println("==================");
    }
    else if (command == "reset") {
      // Emergency reset
      entry.waitingForPermission = false;
      entry.hasPermission = false;
      entry.opening = false;
      entry.closing = false;
      exitBarrier.opening = false;
      exitBarrier.closing = false;
      Serial.println("SYSTEM_RESET");
      updateLCD("System Reset", "Ready");
    }
  }
}

void sendPeriodicSignals() {
  // Send periodic status for entry barrier when car is waiting
  if (entry.waitingForPermission && millis() - lastEntrySignal > SIGNAL_SEND_INTERVAL) {
    Serial.println("CAR_WAITING_ENTRY");
    lastEntrySignal = millis();
  }
}

void setup() {
  Serial.begin(9600);

  // Initialize LCD
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Smart Barrier");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");

  // Initialize pins
  pinMode(ENTRY_TRIG, OUTPUT);
  pinMode(ENTRY_ECHO, INPUT);
  pinMode(ENTRY_SAFE_TRIG, OUTPUT);
  pinMode(ENTRY_SAFE_ECHO, INPUT);

  pinMode(EXIT_TRIG, OUTPUT);
  pinMode(EXIT_ECHO, INPUT);
  pinMode(EXIT_SAFE_TRIG, OUTPUT);
  pinMode(EXIT_SAFE_ECHO, INPUT);

  // Initialize servos
  entryServo.attach(SERVO_ENTRY_PIN);
  exitServo.attach(SERVO_EXIT_PIN);

  entryServo.write(CLOSED_ANGLE);
  exitServo.write(CLOSED_ANGLE);

  delay(2000);

  Serial.println("SYSTEM_READY");
  Serial.println("Commands: plate_valid, plate_invalid, status, reset");

  updateLCD("System Ready", "");
}

void loop() {
  unsigned long now = millis();

  // Update sensors at regular intervals
  if (now - lastSensorUpdate >= SENSOR_UPDATE_INTERVAL) {
    handleEntryBarrier();
    handleExitBarrier();
    lastSensorUpdate = now;
  }

  // Handle serial communication
  handleSerialCommands();

  // Send periodic signals
  sendPeriodicSignals();

  // Small delay to prevent overwhelming the system
  delay(10);
}