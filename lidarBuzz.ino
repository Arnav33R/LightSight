#include <Arduino.h>
#include <Wire.h>
#include <TFLI2C.h>

TFLI2C tflI2C;

int16_t tfDist;                  // distance in centimeters
int16_t tfAddr = TFL_DEF_ADR;    // default I2C address

// setting up the serial port, library, and vibration motor
void setup() {
  pinMode(8, OUTPUT);
  Serial.begin(115200);           // Initialize serial port
  Wire.begin();                   // Initialize Wire library
}

// main event loop to constantly fetch LiDAR sensor readings and turn on the vibration motor accordingly
void loop() {
  if (tflI2C.getData(tfDist, tfAddr)) {
    Serial.print(tfDist);         // Print the distance value
    Serial.println(" cm");
    if (tfDist <= 150) {
      if (tfDist <= 70){
        digitalWrite(8, HIGH);
      }
      else {
      int delayTime = map(tfDist, 70, 150, 300, 1100);  // Map distance to delay time (adjust the range as needed)
      digitalWrite(8, HIGH);
      delay(delayTime);
      digitalWrite(8, LOW);
      delay(delayTime);
      }
    }
    else {
      digitalWrite(8, LOW);
    }
  }
  delay(500);
}
