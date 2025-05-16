from machine import Pin
import time
"""
# Define LED pins
LED_PINS = [2, 4, 5, 18]  # GPIO 2, 4, 5, 18

# Initialize LEDs
leds = [Pin(pin, Pin.OUT) for pin in LED_PINS]

# Main loop
while True:
    for led in leds:
        led.on()   # Turn on current LED
        time.sleep(0.5)  # Wait 0.5 seconds
        led.off()  # Turn off current LED
        
while True:
    for led in leds:
        led.on()
    time.sleep(0.5)
    for led in leds:
        led.off()
    time.sleep(0.5)
    
###########

while True:
    leds[0].on()
    leds[2].on()
    leds[1].off()
    leds[3].off()
    time.sleep(0.5)
    leds[0].off()
    leds[2].off()
    leds[1].on()
    leds[3].on()
    time.sleep(0.5)

##########

"""
# Define LED pin
LED_PIN = 22  # GPIO 2 (often onboard LED)

# Initialize LED
led = Pin(LED_PIN, Pin.OUT)

# Main loop
while True:
    led.on()   # Turn LED on
    time.sleep(0.5)  # Wait 0.5 seconds
    led.off()  # Turn LED off
    time.sleep(0.5)  # Wait 0.5 seconds
    

