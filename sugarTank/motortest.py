from machine import Pin, PWM
import time

# Define GPIO pins for L298N
ENA = Pin(13, Pin.OUT)  # PWM pin for speed control
IN1 = Pin(5, Pin.OUT)   # Direction control 1
IN2 = Pin(4, Pin.OUT)   # Direction control 2

# Set up PWM for speed control
pwm = PWM(ENA, freq=1000, duty=0)  # Frequency 1000 Hz, initial duty cycle 0 (off)

def motor_forward(speed):
    IN1.on()      # Set direction: forward
    IN2.off()
    pwm.duty(speed)  # Set speed (0-1023)

def motor_backward(speed):
    IN1.off()     # Set direction: backward
    IN2.on()
    pwm.duty(speed)  # Set speed (0-1023)

def motor_stop():
    IN1.off()     # Stop motor
    IN2.off()
    pwm.duty(0)   # Set speed to 0

try:
    while True:
        print("Motor Forward")
        motor_forward(512)  # Half speed (512/1023)
        time.sleep(3)       # Run for 3 seconds
        
        print("Motor Stop")
        motor_stop()
        time.sleep(2)       # Stop for 2 seconds
        
        print("Motor Backward")
        motor_backward(768) # 75% speed (768/1023)
        time.sleep(3)       # Run for 3 seconds
        
        print("Motor Stop")
        motor_stop()
        time.sleep(2)       # Stop for 2 seconds

except KeyboardInterrupt:
    motor_stop()
    print("Program stopped")
