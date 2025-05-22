from machine import Pin, PWM
import time

# Define GPIO pins for L298N
# Motor A (first motor)
ENA = Pin(13, Pin.OUT)  # PWM pin for Motor A speed
IN1 = Pin(5, Pin.OUT)   # Motor A direction 1
IN2 = Pin(4, Pin.OUT)   # Motor A direction 2
# Motor B (second motor)
ENB = Pin(12, Pin.OUT)  # PWM pin for Motor B speed
IN3 = Pin(14, Pin.OUT)  # Motor B direction 1
IN4 = Pin(27, Pin.OUT)  # Motor B direction 2

# Set up PWM for speed control
pwm_a = PWM(ENA, freq=1000, duty=0)  # Motor A PWM, 1000 Hz
pwm_b = PWM(ENB, freq=1000, duty=0)  # Motor B PWM, 1000 Hz

# Motor A control functions
def motor_a_forward(speed):
    IN1.on()
    IN2.off()
    pwm_a.duty(speed)  # Speed: 0-1023

def motor_a_backward(speed):
    IN1.off()
    IN2.on()
    pwm_a.duty(speed)

def motor_a_stop():
    IN1.off()
    IN2.off()
    pwm_a.duty(0)

# Motor B control functions
def motor_b_forward(speed):
    IN3.on()
    IN4.off()
    pwm_b.duty(speed)

def motor_b_backward(speed):
    IN3.off()
    IN4.on()
    pwm_b.duty(speed)

def motor_b_stop():
    IN3.off()
    IN4.off()
    pwm_b.duty(0)

try:
    while True:
        print("Both Motors Forward")
        motor_a_forward(512)  # Motor A at 50% speed
        motor_b_forward(512)  # Motor B at 50% speed
        time.sleep(3)         # Run for 3 seconds

        print("Both Motors Stop")
        motor_a_stop()
        motor_b_stop()
        time.sleep(2)         # Stop for 2 seconds

        print("Both Motors Backward")
        motor_a_backward(768) # Motor A at 75% speed
        motor_b_backward(768) # Motor B at 75% speed
        time.sleep(3)         # Run for 3 seconds

        print("Both Motors Stop")
        motor_a_stop()
        motor_b_stop()
        time.sleep(2)         # Stop for 2 seconds

except KeyboardInterrupt:
    motor_a_stop()
    motor_b_stop()
    print("Program stopped")
