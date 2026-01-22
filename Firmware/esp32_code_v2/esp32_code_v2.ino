#define PWMA 6
#define PWMB 16

#define AIN1 7
#define AIN2 15
#define BIN1 17
#define BIN2 18

#define STBY 21

#define PWM_FREQ 1000
#define PWM_RES 8   // 0–255

void setup() {
  Serial.begin(115200);

  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(STBY, OUTPUT);

  digitalWrite(STBY, HIGH); // enable TB6612

  // ESP32 core 3.x PWM
  ledcAttach(PWMA, PWM_FREQ, PWM_RES);
  ledcAttach(PWMB, PWM_FREQ, PWM_RES);

  stopMotors();
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("FWD:")) {
      int pwm = cmd.substring(4).toInt();
      forward(pwm);
    }
    else if (cmd.startsWith("REV:")) {
      int pwm = cmd.substring(4).toInt();
      reverse(pwm);
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

/* -------- Motor control -------- */

void forward(int pwm) {
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);

  ledcWrite(PWMA, pwm);
  ledcWrite(PWMB, pwm);
}

void reverse(int pwm) {
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);

  ledcWrite(PWMA, pwm);
  ledcWrite(PWMB, pwm);
}

void turnLeft() {
  // Left motors STOP, Right motors FORWARD
  ledcWrite(PWMA, 0);
  ledcWrite(PWMB, 120);

  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
}

void turnRight() {
  // Right motors STOP, Left motors FORWARD
  ledcWrite(PWMB, 0);
  ledcWrite(PWMA, 120);

  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
}

void stopMotors() {
  ledcWrite(PWMA, 0);
  ledcWrite(PWMB, 0);
}
