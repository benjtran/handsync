/*
============================================================================
   HandSync - hand_driving.ino
   Author: Benjamin Tran
   Description: Recieve and map hand positions for motor control
============================================================================
*/



#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm;

int NUM_SERVOS = 6;           // Total number of servos to control
int SERVO_MIN = 100;          // Minimum pulse length
int SERVO_MAX = 550;          // Maximum pulse length

// Channels on the PCA9685 board connected to each servo
// Index mapping: 0 = Index, 1 = Middle, 2 = Ring, 3 = Pinky, 4 = Thumb, 5 = Wrist
int servoPins[6] = {0, 1, 2, 3, 4, 6};

void setup() {
  Serial.begin(9600);

  // Initialize PCA9685 driver
  pwm.begin();
  pwm.setPWMFreq(50); // Standard servo frequency is 50 Hz

  // Set initial servo positions
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (i == 4) {
      // Thumb servo initialized to 250
      pwm.setPWM(servoPins[i], 0, 250);
    } else if (i == 5) {
      // Wrist starts at minimum pulse
      pwm.setPWM(servoPins[5], 0, SERVO_MIN);
    } else {
      // Fingers start fully extended
      pwm.setPWM(servoPins[i], 0, SERVO_MAX);
    }
  }

  // Give servos time to move to their start positions
  delay(2000);
}

void loop() {
  // If data is available from the serial port (from PC/Python)
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n'); // Read the entire line of angle data
    line.trim(); // Remove whitespace/newlines
    int angles[6]; // Array to hold parsed angles
    int i = 0;

    // Parse comma-separated angles into the array
    for (int start = 0; start < line.length(); ) {
      int end = line.indexOf(',', start);
      if (end == -1) end = line.length(); // Handle last value
      angles[i++] = line.substring(start, end).toInt(); // Convert substring to integer
      start = end + 1;
    }

    // Map each angle to a servo PWM value and write to the respective servo
    int wrist_pulse = map(angles[0], 0, 180, SERVO_MIN, (SERVO_MIN + SERVO_MAX)/1.5);
    int thumb_pulse = map(angles[5], 50, 180, SERVO_MIN, 250); // Thumb mapped within a limited range

    // Assign PWM signals to each servo based on angle input
    pwm.setPWM(servoPins[5], 0, wrist_pulse); // Wrist servo (channel 6)
    pwm.setPWM(servoPins[0], 0, map(angles[1], 0, 180, SERVO_MIN, SERVO_MAX)); // Index
    pwm.setPWM(servoPins[1], 0, map(angles[2], 0, 180, SERVO_MIN, SERVO_MAX)); // Middle
    pwm.setPWM(servoPins[2], 0, map(angles[3], 0, 180, SERVO_MIN, SERVO_MAX)); // Ring
    pwm.setPWM(servoPins[3], 0, map(angles[4], 0, 180, SERVO_MIN, SERVO_MAX)); // Pinky
    pwm.setPWM(servoPins[4], 0, thumb_pulse); // Thumb (limited mapping range)
  }
}