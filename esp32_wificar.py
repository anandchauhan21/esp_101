from machine import Pin, PWM
import network
import socket

# Motor A (left motor)
motorA_in1 = Pin(5, Pin.OUT)  # D1 = GPIO5
motorA_in2 = Pin(4, Pin.OUT)  # D2 = GPIO4
motorA_ena = PWM(Pin(14), freq=1000)  # D5 = GPIO14

# Motor B (right motor)
motorB_in3 = Pin(12, Pin.OUT)  # D6 = GPIO12
motorB_in4 = Pin(13, Pin.OUT)  # D7 = GPIO13
motorB_enb = PWM(Pin(15), freq=1000)  # D8 = GPIO15

# Wi-Fi credentials
SSID = "iQOO"
PASSWORD = "1234567890"
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)  # Reset Wi-Fi module
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Connected to Wi-Fi:", wlan.ifconfig())
    return wlan.ifconfig()[0]


# HTML for the web interface
html = """<!DOCTYPE html>
<html>
<head>
    <title>Car Control</title>
    <style>
        body { font-family: Arial; text-align: center; }
        button { padding: 20px; margin: 10px; font-size: 18px; }
    </style>
</head>
<body>
    <h1>Car Control</h1>
    <button onclick="sendRequest('forward')">Forward</button><br>
    <button onclick="sendRequest('left')">Left</button>
    <button onclick="sendRequest('stop')">Stop</button>
    <button onclick="sendRequest('right')">Right</button><br>
    <button onclick="sendRequest('backward')">Backward</button>
    <script>
        function sendRequest(direction) {
            fetch('/' + direction).then(response => console.log(direction + " command sent"));
        }
    </script>
</body>
</html>
"""

def control_motors(direction):
    if direction == "forward":
        motorA_in1.on()
        motorA_in2.off()
        motorA_ena.duty(512)  # Adjust duty cycle for speed (0-1023)
        
        motorB_in3.on()
        motorB_in4.off()
        motorB_enb.duty(512)  # Adjust duty cycle for speed (0-1023)
    elif direction == "backward":
        motorA_in1.off()
        motorA_in2.on()
        motorA_ena.duty(512)
        
        motorB_in3.off()
        motorB_in4.on()
        motorB_enb.duty(512)
    elif direction == "left":
        motorA_in1.off()
        motorA_in2.off()
        motorA_ena.duty(0)
        
        motorB_in3.on()
        motorB_in4.off()
        motorB_enb.duty(512)
    elif direction == "right":
        motorA_in1.on()
        motorA_in2.off()
        motorA_ena.duty(512)
        
        motorB_in3.off()
        motorB_in4.off()
        motorB_enb.duty(0)
    else:  # Stop
        motorA_in1.off()
        motorA_in2.off()
        motorA_ena.duty(0)
        
        motorB_in3.off()
        motorB_in4.off()
        motorB_enb.duty(0)

def serve():
    ip = connect_wifi()
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print("Listening on", addr)

    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        request = cl.recv(1024).decode()
        print("Request:", request)
        
        # Parse the request
        if "GET /forward" in request:
            control_motors("forward")
        elif "GET /backward" in request:
            control_motors("backward")
        elif "GET /left" in request:
            control_motors("left")
        elif "GET /right" in request:
            control_motors("right")
        elif "GET /stop" in request:
            control_motors("stop")
        
        # Respond with the HTML page
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(html)
        cl.close()

# Start the server
serve()

