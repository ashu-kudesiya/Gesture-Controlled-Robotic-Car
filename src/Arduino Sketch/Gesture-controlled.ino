#include <AFMotor.h>
#include <SoftwareSerial.h>


#define BT_RX_PIN 0 // Connect HC-05 TX to Arduino pin 0(motor driver)
#define BT_TX_PIN 1 // Connect HC-05 RX to Arduino pin 1(motor driver)

SoftwareSerial BTSerial(BT_RX_PIN, BT_TX_PIN); // Create a SoftwareSerial object for Bluetooth communication

AF_DCMotor motor1(1); // Create motor objects for 4 motors
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void setup() {
  Serial.begin(9600); // Start serial communication for debugging
  BTSerial.begin(9600); // Start Bluetooth serial communication
  
  // Set up motor controller pins
  motor1.setSpeed(255); // Set the motor speed (0-255)
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
  
  pinMode(BUZZER_PIN, OUTPUT); // Set the buzzer pin as output
}

void loop() {
  if (BTSerial.available()) { // Check if data is available from Bluetooth
    char command = BTSerial.read(); // Read the incoming command

    // Switch case to handle different commands
    switch (command) {
      case '5':
        moveForward(); // Move all motors forward
        break;
      case '4':
        moveBackward(); // Move all motors backward
        break;
      case '0':
        stopMotors(); // Stop all motors
        break;
      case '1':
        turnLeft(); // Make a left turn
        break;
      case '2':
        turnRight(); // Make a right turn
        break;
    }
  }
}

void moveForward() {
  motor1.run(FORWARD); // Run motor 1 forward
  motor2.run(FORWARD); // Run motor 2 forward
  motor3.run(FORWARD); // Run motor 3 forward
  motor4.run(FORWARD); // Run motor 4 forward
}

void moveBackward() {
  motor1.run(BACKWARD); // Run motor 1 backward
  motor2.run(BACKWARD); // Run motor 2 backward
  motor3.run(BACKWARD); // Run motor 3 backward
  motor4.run(BACKWARD); // Run motor 4 backward
}

void stopMotors() {
  motor1.run(RELEASE); // Release motor 1
  motor2.run(RELEASE); // Release motor 2
  motor3.run(RELEASE); // Release motor 3
  motor4.run(RELEASE); // Release motor 4
}

void turnLeft() {
  // Stop motor 1 and 2
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  // Run motor 3 and 4 forward
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void turnRight() {
  // Stop motor 3 and 4
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  // Run motor 1 and 2 forward
  motor1.run(FORWARD);
  motor2.run(FORWARD);
}

