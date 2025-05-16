from machine import Pin, time_pulse_us
import time

# Define TRIG and ECHO pins for HC-SR04
TRIG_PIN = 22   # GPIO 5
ECHO_PIN = 23  # GPIO 18

# Initialize pins
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def measure_distance():
    # Ensure trigger is low
    trig.off()
    time.sleep_us(2)
    
    # Send 10us trigger pulse
    trig.on()
    time.sleep_us(10)
    trig.off()
    
    # Measure echo pulse duration
    pulse_duration = time_pulse_us(echo, 1, 30000)  # Timeout after 30ms
    
    if pulse_duration < 0:
        return None  # No echo received (object too far or error)
    
    # Calculate distance (speed of sound = 343 m/s = 0.0343 cm/us)
    distance_cm = (pulse_duration / 2) * 0.0343
    
    return distance_cm

# Main loop
while True:
    distance = measure_distance()
    
    if distance is None:
        print("No echo received (out of range or error)")
    else:
        print(f"Distance: {distance:.1f} cm")
    
    time.sleep(0.1)  # Wait 100ms between measurements
