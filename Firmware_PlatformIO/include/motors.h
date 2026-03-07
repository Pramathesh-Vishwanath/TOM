#ifndef MOTORS_H
#define MOTORS_H

#include <Arduino.h>

// Pin Definitions
#define PWMA 6
#define PWMB 16
#define AIN1 7
#define AIN2 15
#define BIN1 17
#define BIN2 18
#define STBY 21

void initMotors();
void forward(int pwm);
void reverse(int pwm);
void turnLeft();
void turnRight();
void stopMotors();

#endif
