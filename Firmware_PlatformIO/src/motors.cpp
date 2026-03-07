#include <Arduino.h>
#include "motors.h"

#define PWM_FREQ 1000
#define PWM_RES 8

#define CH_A 0
#define CH_B 1

void initMotors() {
    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(BIN1, OUTPUT);
    pinMode(BIN2, OUTPUT);
    pinMode(STBY, OUTPUT);

    digitalWrite(STBY, HIGH);

    ledcSetup(CH_A, PWM_FREQ, PWM_RES);
    ledcAttachPin(PWMA, CH_A);

    ledcSetup(CH_B, PWM_FREQ, PWM_RES);
    ledcAttachPin(PWMB, CH_B);

    stopMotors();
}
void forward(int pwm) {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    ledcWrite(CH_A, pwm);
    ledcWrite(CH_B, pwm);
}

void reverse(int pwm) {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    ledcWrite(CH_A, pwm);
    ledcWrite(CH_B, pwm);
}

void turnLeft() {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    ledcWrite(CH_A, 255);
    ledcWrite(CH_B, 255);
}

void turnRight() {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    ledcWrite(CH_A, 255);
    ledcWrite(CH_B, 255);
}

void stopMotors() {
    ledcWrite(CH_A, 0);
    ledcWrite(CH_B, 0);
}
