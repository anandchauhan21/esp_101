from machine import Pin, PWM
import time

# Define GPIO pins for L298N
# Motor A (left motor)
ENA = Pin(13, Pin.OUT)  # PWM pin for Motor A speed
IN1 = Pin(5, Pin.OUT)   # Motor A direction 1
IN2 = Pin(4, Pin.OUT)   # Motor A direction 2
# Motor B (right motor)
ENB = Pin(12, Pin.OUT)  # PWM pin for Motor B speed
IN3 = Pin(14, Pin.OUT)  # Motor B direction 1
IN4 = Pin(27, Pin.OUT)  # Motor B direction 2

# Set up PWM for speed control
pwm_a = PWM(ENA, freq=1000, duty=0)  # Motor A PWM, 1000 Hz
pwm_b = PWM(ENB, freq=1000, duty=0)  # Motor B PWM, 1000 Hz

# Motor A (left) control functions
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

# Motor B (right) control functions
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

# Function to move robot forward
def move_forward(speed, duration):
    print("Moving Forward")
    motor_a_forward(speed)
    motor_b_forward(speed)
    time.sleep(duration)
    motor_a_stop()
    motor_b_stop()

# Function to turn right 90 degrees (stop left motor, run right motor)
def turn_right(speed, duration):
    print("Turning Right")
    motor_a_stop()       # Left motor stops
    motor_b_forward(speed)  # Right motor runs
    time.sleep(duration)
    motor_b_stop()

# Function to trace a square (4 sides)
def trace_square():
    speed = 512  # 50% speed (adjust as needed)
    forward_time = 2.0  # Time to move forward (seconds, adjust for side length)
    turn_time = 0.5     # Time to turn 90 degrees (seconds, adjust for wheelbase)

    for _ in range(4):  # Repeat 4 times for a square
        move_forward(speed, forward_time)
        time.sleep(0.5)  # Short pause between movements
        turn_right(speed, turn_time)
        time.sleep(0.5)  # Short pause after turn

try:
    print("Starting square path")
    trace_square()
    print("Square complete")
except KeyboardInterrupt:
    motor_a_stop()
    motor_b_stop()
    print("Program stopped")
finally:
    motor_a_stop()
    motor_b_stop()  # Ensure motors stop on exit
