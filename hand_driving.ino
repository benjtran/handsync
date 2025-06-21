#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm;

int NUM_SERVOS = 6;
int SERVO_MIN = 100;
int SERVO_MAX = 550;

int servoPins[6] = {0, 1, 2, 3, 4, 6};

void setup() {
  Serial.begin(9600);

  //Defining servos
  pwm.begin();
  pwm.setPWMFreq(50);


  for (int i = 0; i < NUM_SERVOS; i++) {
    if (i == 4) {
      pwm.setPWM(servoPins[i], 0, 250);
    } else if (i == 5) {
      pwm.setPWM(servoPins[5], 0, SERVO_MIN);
    } else {
      pwm.setPWM(servoPins[i], 0, SERVO_MAX);
    }
  }
  delay(2000);
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim(); // Remove whitespace
    int angles[6];
    int i = 0;
    for (int start = 0; start < line.length(); ) {
      int end = line.indexOf(',', start);
      if (end == -1) end = line.length();
      angles[i++] = line.substring(start, end).toInt();
      start = end + 1;
    }

    int wrist_pulse = map(angles[0], 0, 180, SERVO_MIN, (SERVO_MIN + SERVO_MAX)/1.5);
    int thumb_pulse = map(angles[5], 50, 180, SERVO_MIN, 250);
    pwm.setPWM(servoPins[5], 0, wrist_pulse);
    pwm.setPWM(servoPins[0], 0, map(angles[1], 0, 180, SERVO_MIN, SERVO_MAX));
    pwm.setPWM(servoPins[1], 0, map(angles[2], 0, 180, SERVO_MIN, SERVO_MAX));
    pwm.setPWM(servoPins[2], 0, map(angles[3], 0, 180, SERVO_MIN, SERVO_MAX));
    pwm.setPWM(servoPins[3], 0, map(angles[4], 0, 180, SERVO_MIN, SERVO_MAX));
    pwm.setPWM(servoPins[4], 0, thumb_pulse);
  }
}
  /*if (Serial.available() > 0) {
    //---------------------------------WRIST MOVEMENT---------------------------------------
    String str_wrist_angle = Serial.readStringUntil('\n');
    int wrist_angle = str_wrist_angle.toInt();
    int wrist_pulse = map(wrist_angle, 0, 180, SERVO_MIN, (SERVO_MIN + SERVO_MAX)/1.5);
    pwm.setPWM(servoPins[5], 0, wrist_pulse);

    //---------------------------------POINTER MOVEMENT---------------------------------------
    String str_pointer_angle = Serial.readStringUntil('\n');
    int pointer_angle = str_pointer_angle.toInt();
    int pointer_pulse = map(pointer_angle, 0, 180, SERVO_MIN, SERVO_MAX);
    pwm.setPWM(servoPins[0], 0, pointer_pulse);

    //---------------------------------MIDDLE MOVEMENT---------------------------------------
    String str_middle_angle = Serial.readStringUntil('\n');
    int middle_angle = str_middle_angle.toInt();
    int middle_pulse = map(middle_angle, 0, 180, SERVO_MIN, SERVO_MAX);
    pwm.setPWM(servoPins[1], 0, middle_pulse);

    //---------------------------------RING MOVEMENT---------------------------------------
    String str_ring_angle = Serial.readStringUntil('\n');
    int ring_angle = str_ring_angle.toInt();
    int ring_pulse = map(ring_angle, 0, 180, SERVO_MIN, SERVO_MAX);
    pwm.setPWM(servoPins[2], 0, ring_pulse);

     //---------------------------------PINKY MOVEMENT---------------------------------------
    String str_pinky_angle = Serial.readStringUntil('\n');
    int pinky_angle = str_pinky_angle.toInt();
    int pinky_pulse = map(pinky_angle, 0, 180, SERVO_MIN, SERVO_MAX);
    pwm.setPWM(servoPins[3], 0, pinky_pulse);
  }
}

  /*
  for (int pos = 270; pos >= 0; pos--) {
    int pulse = map(pos, 0, 270, SERVO_MIN, SERVO_MAX);
    int thumbPulse = map(pos, 0, 270, SERVO_MIN, 250);
    for (int i = 0; i < NUM_SERVOS; i++) {
      if (i == 4) {
        pwm.setPWM(servoPins[i], 0, thumbPulse);
      } else {
        pwm.setPWM(servoPins[i], 0, pulse);
      }
    }
    delay(20);
  }
  for (int pos = 0; pos <= 270; pos++) {
    int pulse = map(pos, 0, 270, SERVO_MIN, SERVO_MAX);
    int thumbPulse = map(pos, 0, 270, SERVO_MIN, 250);
    for (int i = 0; i < NUM_SERVOS; i++) {
      if (i == 4) {
        pwm.setPWM(servoPins[i], 0, thumbPulse);
      } else {
        pwm.setPWM(servoPins[i], 0, pulse);
      }
    }
    delay(20);
  }
  delay(3000);
  */