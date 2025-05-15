from machine import Pin, PWM

# Configure PWM pin for servo (e.g., GPIO 15)
servo_pin = Pin(19)
servo = PWM(servo_pin, freq=50)  # 50Hz for servo

def set_servo_angle(angle):
    # Ensure angle is within 0-180 degrees
    angle = max(0, min(180, angle))
    # Convert angle to duty cycle (2.5%-12.5% of 50Hz)
    # Duty range: ~500-2500us (1024 = 20ms, so 25-125)
    duty = int(25 + (angle / 180) * 100)
    servo.duty(duty)
    print(f"Servo set to {angle} degrees")

# Main loop
try:
    while True:
        # Get angle input from user
        angle_str = input("Enter angle (0-180 degrees, or 'q' to quit): ")
        
        # Check for quit command
        if angle_str.lower() == 'q':
            break
            
        # Try to convert input to integer and set angle
        try:
            angle = int(angle_str)
            if 0 <= angle <= 180:
                set_servo_angle(angle)
            else:
                print("Error: Angle must be between 0 and 180 degrees")
        except ValueError:
            print("Error: Please enter a valid number or 'q' to quit")

except KeyboardInterrupt:
    print("\nProgram terminated")

finally:
    # Cleanup on exit
    servo.deinit()
    print("Servo PWM deinitialized")
