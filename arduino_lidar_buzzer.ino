#include <Arduino.h>
#include <Wire.h>
#include <TFLI2C.h>

TFLI2C tflI2C;

int16_t tfDist;                  // distance in centimeters
int16_t tfAddr = TFL_DEF_ADR;    // Use this default I2C address

void setup() {
  pinMode(8, OUTPUT);
  Serial.begin(9600);           // Initialize serial port
  Wire.begin();                   // Initialize Wire library
}

void loop() {
  if (tflI2C.getData(tfDist, tfAddr)) {
    Serial.print(tfDist);         // Print the distance value
    Serial.println(" cm");
    if (tfDist >= 50) {
      digitalWrite(8, HIGH);
    }
    else {
      digitalWrite(8, LOW);
    }
  }
  delay(500);
}
