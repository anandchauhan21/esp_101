from machine import Pin
import time

# Define buzzer pin
BUZZER_PIN = 22  # GPIO 2

# Initialize buzzer pin
buzzer = Pin(BUZZER_PIN, Pin.OUT)

# Main loop
while True:
    buzzer.on()   # Turn buzzer on
    time.sleep(0.5)  # Beep for 0.5 seconds
    buzzer.off()  # Turn buzzer off
    time.sleep(0.5)  # Wait 0.5 seconds before next beep
