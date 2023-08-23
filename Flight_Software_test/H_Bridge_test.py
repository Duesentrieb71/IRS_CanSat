from machine import Pin
import time

# Motor H-Brücke (GP16/GP17)
motor_1 = Pin(16, Pin.OUT)
motor_2 = Pin(17, Pin.OUT)

# test motor
motor_1.value(1)
motor_2.value(0)
print("Motor 1")
time.sleep(2)
motor_1.value(0)
motor_2.value(1)
print("Motor 2")
time.sleep(2)
motor_1.value(1)
motor_2.value(1)
print("Motor 1 and 2")
time.sleep(2)
motor_1.value(0)
motor_2.value(0)
print("Motor 0")
