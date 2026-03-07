#include "motors.h"

#define PWM_FREQ 1000
#define PWM_RES 8

void initMotors() {
    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(BIN1, OUTPUT);
    pinMode(BIN2, OUTPUT);
    pinMode(STBY, OUTPUT);
    digitalWrite(STBY, HIGH);

    ledcAttach(PWMA, PWM_FREQ, PWM_RES);
    ledcAttach(PWMB, PWM_FREQ, PWM_RES);
    stopMotors();
}

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
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    ledcWrite(PWMA, 255);
    ledcWrite(PWMB, 255);
}

void turnRight() {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    ledcWrite(PWMA, 255);
    ledcWrite(PWMB, 255);
}

void stopMotors() {
    ledcWrite(PWMA, 0);
    ledcWrite(PWMB, 0);
}
