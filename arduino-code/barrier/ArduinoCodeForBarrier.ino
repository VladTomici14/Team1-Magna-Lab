#include <Servo.h>
#include <LiquidCrystal_I2C.h>

#define SERVO_PIN 6
#define CLOSED_ANGLE 0
#define OPEN_ANGLE 65
#define STEP_DELAY_MS 15

#define PUSHBUTTON_PIN 5
#define GREEN_LED_PIN 2
#define RED_LED_PIN 3
#define BUTTON_DEBOUNCE_DELAY 100
#define ULTRASONIC_DELAY 100
#define BUFFER_SIZE      5


Servo barrierServo;
LiquidCrystal_I2C lcd(0x27,16,2);

int mappedAngle;

bool buttonState = false;
bool lastButtonReading = false;
unsigned long lastDebounceTime = 0;
bool OK;

const int trigPin1 = 11;
const int echoPin1 = 12;
const int trigPin2 = 9;
const int echoPin2 = 10;

float duration, distance;
unsigned long now = 0;
unsigned long then = 0;

int Sensor1ReadingValid = 0;
int Sensor2ReadingValid = 0;

int ultrasonicReadingBuffer1[BUFFER_SIZE] = {0};
int ultrasonicReadingBuffer2[BUFFER_SIZE] = {0};
bool BarrierIsNowOpened = false;

int carBefore = 0;
int carAfter = 0;
int carAfter_LastValue =0;  

int index1=0;
int index2=0;


bool barrierIsOpening = false;
bool barrierIsClosing = false;

unsigned long lastMoveTime = 0;
int barrierAngle = CLOSED_ANGLE; 

String lastLine1 = "";
String lastLine2 = "";
void handleButton() {
  bool reading = digitalRead(PUSHBUTTON_PIN) == HIGH;  // Active LOW button

  if (reading != lastButtonReading) {
    lastDebounceTime = millis();  // reset debounce timer
  }

  if ((millis() - lastDebounceTime) > BUTTON_DEBOUNCE_DELAY) {
    if (reading != buttonState) {

      buttonState = reading;

      if (buttonState) {
        OK = !OK;
      }
    }
  }


  lastButtonReading = reading;
}


void licensePlateIsOk() {
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, HIGH);
  openBarrier();
}




void licensePlateIsNotOk() {
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, HIGH);
  //closeBarrier();  // Optional: close if not OK
}




void openBarrier() {
  BarrierIsNowOpened = true;
  barrierIsOpening = true;
  barrierIsClosing = false;
  BarrierLed();  // Optional visual indicator
  OK = false;
 
}





void closeBarrier() {
  BarrierIsNowOpened = false;
  barrierIsClosing = true;
  barrierIsOpening = false;
  BarrierLed();  // Optional visual indicator
}

void updateBarrier() {
  unsigned long now = millis();

  if ((barrierIsOpening || barrierIsClosing) && now - lastMoveTime >= STEP_DELAY_MS) {
    lastMoveTime = now;

    if (barrierIsOpening) {
      if (barrierAngle < OPEN_ANGLE) {
        barrierAngle++;
        int mappedAngle = map(barrierAngle, 0, 180, 0, 255);
        barrierServo.write(mappedAngle);
      } else {
        barrierIsOpening = false;  // Finished
      }
    }

    if (barrierIsClosing) {
      if (barrierAngle > CLOSED_ANGLE) {
        barrierAngle--;
        int mappedAngle = map(barrierAngle, 0, 180, 0, 255);
        barrierServo.write(mappedAngle);
      } else {
        barrierIsClosing = false;  // Finished
      }
    }
  }
}

void  updatePresentCarState(int readingValidation, int* buffer,int*index,int *carPresent) {
  
  
  buffer[*index] = readingValidation;
  (*index)++;

  if (*index >= BUFFER_SIZE) 
  {
    int sum = 0;
    for (int i = 0; i < BUFFER_SIZE; i++) {
      sum += buffer[i];
    }

    if(sum >= BUFFER_SIZE-1)
       *carPresent=1;
      else
       *carPresent=0;
        // 9/10 consistent readings = car present
    *index = 0;
  }

  
}




int ReadUltrasonic(int echoPin, int trigPin) {
  // Trigger ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read echo duration
  long duration = pulseIn(echoPin, HIGH, 30000);  // 30ms timeout
  float distance = (duration * 0.0343) / 2.0;     // Convert to cm

  // Return presence detection (1 if car present, 0 otherwise)
  return (distance > 0 && distance < 20) ? 1 : 0;
}

void BarrierLed()
{
if(BarrierIsNowOpened ==false)
  {
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, HIGH);
  }

if(BarrierIsNowOpened ==true)
  {
   digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, HIGH);
  }


}





int getCenter(const String& text) {
  int len = text.length();
  return max(0, (16 - len) / 2);
}

void updateLCDStatus(bool carBefore, bool carAfter, bool barrierOpened, bool okRequested, bool BarrierIsOpening, bool BarrierIsClosing) {
  String line1, line2;

 if (BarrierIsOpening)
  {
    line1 = "Access granted";
    line2 = "Barrier is opening";
  } else if (carBefore && !barrierOpened && !okRequested)
  {
    line1 = "Car detected";
    line2 = "Press Button";
  } else if (barrierOpened && carAfter) 
  {
    line1 = "Car in zone";
    line2 = "Barrier is opened";
  } else if (BarrierIsClosing) 
  {
    line1 = "Car passed";
    line2 = "Closing barrier";
  } else if (!carBefore && !carAfter && !barrierOpened) 
  {
    line1 = "HELLO";
    line2 = "";
  }
  else if(carBefore && barrierOpened)
  {
    line1 = "MOVE FORWARD->->->";
    line2 = "";
  }

  // Only update display if lines have changed
  if (line1 != lastLine1 || line2 != lastLine2) {
    lcd.clear();
    lcd.setCursor(getCenter(line1), 0);
    lcd.print(line1);
    lcd.setCursor(getCenter(line2), 1);
    lcd.print(line2);
    lastLine1 = line1;
    lastLine2 = line2;
  }
}

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  pinMode(PUSHBUTTON_PIN, INPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);

  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);


  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);

  barrierServo.attach(SERVO_PIN);
  barrierServo.write(CLOSED_ANGLE);  // Start closed



  lcd.begin();
lcd.backlight();
lcd.clear();
lcd.setCursor(0, 0);
lcd.print("System Ready");
  delay(1000);
}

void loop() {



  now = millis();

  if (now - then > ULTRASONIC_DELAY) {



    Sensor1ReadingValid = ReadUltrasonic(echoPin1, trigPin1);
   updatePresentCarState(Sensor1ReadingValid, ultrasonicReadingBuffer1,&index1,&carBefore);


    Sensor2ReadingValid = ReadUltrasonic(echoPin2, trigPin2);
    updatePresentCarState(Sensor2ReadingValid, ultrasonicReadingBuffer2,&index2,&carAfter);

    

      

    then = now;
  }





  if (carBefore == 1&& BarrierIsNowOpened ==false) 
  {

    handleButton();
    if (OK)
      openBarrier();
   
  }

    if(carAfter_LastValue==1 && carAfter==0&& BarrierIsNowOpened ==true)
      closeBarrier();
   
      

    
    carAfter_LastValue=carAfter;
    updateLCDStatus(carBefore, carAfter, BarrierIsNowOpened, OK,barrierIsOpening,barrierIsClosing);
    updateBarrier();
    BarrierLed();
}
