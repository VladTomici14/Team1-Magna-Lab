#include <Servo.h>

#define DELAY 250
#define FEEDBACK_THRESHOLD 3      
#define GARBAGE_THRESHOLD 50      
#define GARBAGE_LIMIT 4          

Servo myServo;
int potPin = A1;
int servoPin = 9;
int feedbackPin = A3;

unsigned long now = 0;
unsigned long then = 0;

int OldInput = 0;
int NewInput = 0;
int Error = 0;

int OldFeedback = 0;
int NewFeedback = 0;

int stableErrorCount = 0;     // Stuck error
int garbageErrorCount = 0;    // Garbage feedback error

int stableErrorLimit = 4;     // How many times before declaring error

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  OldInput = analogRead(potPin);
  OldFeedback = analogRead(feedbackPin);
}

void loop() {
  int potValue = analogRead(potPin);
  NewInput = potValue;
  int angle = map(potValue, 0, 1023, 0, 180);
  myServo.write(angle);

  NewFeedback = analogRead(feedbackPin);

  now = millis();
  if (now - then > DELAY) 
  {

    if (abs(NewInput - OldInput) > 10) 
    {
      if (abs(NewFeedback - OldFeedback) < FEEDBACK_THRESHOLD) 
      {
        stableErrorCount++;
        if (stableErrorCount >= stableErrorLimit)
          Error = 1;
      } 
      else
        stableErrorCount = 0;
    } 
    else
      stableErrorCount = 0;

 
    if (abs(NewInput - OldInput) < 10) // Input stable
    {
      if (abs(NewFeedback - OldFeedback) > GARBAGE_THRESHOLD) 
      {
        garbageErrorCount++;
        if (garbageErrorCount >= GARBAGE_LIMIT)
          Error = 2;
      } 
      else
        garbageErrorCount = 0;
    }
    else
      garbageErrorCount = 0;

    
    if (Error == 1)
      Serial.println("!!!!!!!!!!!!!!SERVO ERROR (Signal Cutoff)!!!!!!!!!!!!!");
    else if (Error == 2)
      Serial.println("!!!!!!!!!!!!!!SERVO ERROR (Power Cutoff)!!!!!!!!!!!!!");
    else
    {   
      Serial.print("Input: ");
      Serial.print(NewInput);
      Serial.print("\tFeedback: ");
      Serial.println(NewFeedback);
    }

    OldInput = NewInput;
    OldFeedback = NewFeedback;
    then = now;
  }
}
