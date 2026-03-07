#include <Arduino.h>
#include "motors.h"

void setup() {
  Serial.begin(115200);
  initMotors();
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("FWD:")) {
      forward(cmd.substring(4).toInt());
    }
    else if (cmd.startsWith("REV:")) {
      reverse(cmd.substring(4).toInt());
    }
    else if (cmd == "LEFT") {
      turnLeft();
    }
    else if (cmd == "RIGHT") {
      turnRight();
    }
    else if (cmd == "STOP") {
      stopMotors();
    }
  }
}
