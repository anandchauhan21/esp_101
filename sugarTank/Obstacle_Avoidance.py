from machine import Pin, time_pulse_us
from time import sleep_us, sleep

# Motor pins
in1 = Pin(16, Pin.OUT)
in2 = Pin(17, Pin.OUT)
in3 = Pin(19, Pin.OUT)
in4 = Pin(21, Pin.OUT)

# HC-SR04 pins
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

def get_distance():
    trig.off()
    sleep_us(2)
    trig.on()
    sleep_us(10)
    trig.off()

    duration = time_pulse_us(echo, 1, 30000)  # timeout 30ms
    distance = (duration * 0.0343) / 2  # cm
    return distance

# Motor control functions
def stop():
    in1.off(); in2.off(); in3.off(); in4.off()

def forward():
    in1.on(); in2.off()
    in3.on(); in4.off()

def backward():
    in1.off(); in2.on()
    in3.off(); in4.on()

def turn_right():
    in1.on(); in2.off()
    in3.off(); in4.on()

def turn_left():
    in1.off(); in2.on()
    in3.on(); in4.off()

# Main loop
while True:
    distance = get_distance()
    print("Distance:", distance, "cm")
    if distance < 20:  # obstacle detected
        stop()
        sleep(0.3)
        backward()
        sleep(0.7)
        turn_right()
        sleep(0.7)
        stop()
        sleep(0.2)
    else:
        forward()
