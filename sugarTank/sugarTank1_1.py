from machine import Pin, PWM
import time
import network
import socket

# Motor A (left motor)
motorA_in1 = Pin(17, Pin.OUT)  # D1 = GPIO5
motorA_in2 = Pin(5, Pin.OUT)  # D2 = GPIO4
motorA_ena = PWM(Pin(18), freq=1000)  # D5 = GPIO14

# Motor B (right motor)
motorB_in3 = Pin(4, Pin.OUT)  # D6 = GPIO12
motorB_in4 = Pin(2, Pin.OUT)  # D7 = GPIO13
motorB_enb = PWM(Pin(15), freq=1000)  # D8 = GPIO15

# Default speeds
speedA = 512  # 50% duty cycle
speedB = 512  # 50% duty cycle

# Moter Driver mode
St_by = Pin(16,Pin.OUT)
St_by.on()

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
    <title>Car Control - Gamepad</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 10px;
            box-sizing: border-box;
            background: #e0e0e0;
            touch-action: manipulation;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        h1 {
            font-size: 1.4em;
            margin: 10px 0;
            color: #333;
            text-align: center;
        }
        .gamepad {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 360px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .dpad {
            display: grid;
            grid-template-areas:
                ". up ."
                "left stop right"
                ". down .";
            grid-gap: 12px;
            width: 180px;
            height: 180px;
            margin-bottom: 20px;
        }
        .dpad button {
            border: none;
            border-radius: 12px;
            background: linear-gradient(145deg, #ffffff, #e6e6e6);
            box-shadow: 3px 3px 6px rgba(0,0,0,0.2), -3px -3px 6px rgba(255,255,255,0.5);
            cursor: pointer;
            touch-action: none;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            transition: transform 0.1s;
        }
        .dpad button:active {
            background: linear-gradient(145deg, #e6e6e6, #ffffff);
            transform: scale(0.95);
        }
        .dpad svg {
            width: 30px;
            height: 30px;
            fill: none;
            stroke: #333;
            stroke-width: 3;
            stroke-linecap: round;
            stroke-linejoin: round;
        }
        .up { grid-area: up; }
        .left { grid-area: left; }
        .stop { grid-area: stop; }
        .right { grid-area: right; }
        .down { grid-area: down; }
        .speed-controls {
            display: flex;
            flex-direction: column;
            width: 100%;
            max-width: 280px;
        }
        .slider-container {
            margin: 10px 0;
        }
        label {
            font-size: 12px;
            color: #333;
            margin-bottom: 5px;
            display: block;
            text-align: center;
        }
        input[type="range"] {
            width: 100%;
            -webkit-appearance: none;
            background: #ddd;
            border-radius: 5px;
            height: 10px;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            background: #333;
            border-radius: 50%;
            cursor: pointer;
        }
        input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            background: #333;
            border-radius: 50%;
            cursor: pointer;
        }
        @media (max-width: 360px) {
            .gamepad {
                transform: scale(0.85);
                padding: 15px;
            }
            h1 {
                font-size: 1.2em;
            }
            .dpad {
                width: 140px;
                height: 140px;
            }
            .dpad svg {
                width: 24px;
                height: 24px;
                stroke-width: 2.5;
            }
            .speed-controls {
                max-width: 240px;
            }
        }
    </style>
</head>
<body>
    <h1>Car Control</h1>
    <div class="gamepad">
        <div class="dpad">
            <button class="up" onclick="sendRequest('forward')">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2 L12 22 M2 12 L12 2 L22 12" />
                </svg>
            </button>
            <button class="left" onclick="sendRequest('left')">
                <svg viewBox="0 0 24 24">
                    <path d="M2 12 L22 12 M12 2 L2 12 L12 22" />
                </svg>
            </button>
            <button class="stop" onclick="sendRequest('stop')">
                <svg viewBox="0 0 24 24">
                    <rect x="6" y="6" width="12" height="12" />
                </svg>
            </button>
            <button class="right" onclick="sendRequest('right')">
                <svg viewBox="0 0 24 24">
                    <path d="M2 12 L22 12 M12 2 L22 12 L12 22" />
                </svg>
            </button>
            <button class="down" onclick="sendRequest('backward')">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2 L12 22 M2 12 L12 22 L22 12" />
                </svg>
            </button>
        </div>
        <div class="speed-controls">
            <div class="slider-container">
                <label>Left Motor</label>
                <input type="range" min="0" max="1023" value="512" id="speedA" onchange="updateSpeed('A')">
            </div>
            <div class="slider-container">
                <label>Right Motor</label>
                <input type="range" min="0" max="1023" value="512" id="speedB" onchange="updateSpeed('B')">
            </div>
        </div>
    </div>
    <script>
        function sendRequest(direction) {
            fetch('/' + direction)
                .then(response => console.log(direction + " command sent"))
                .catch(error => console.error("Error sending " + direction + " command:", error));
        }
        function updateSpeed(motor) {
            let speed = motor === 'A' ? document.getElementById('speedA').value : document.getElementById('speedB').value;
            fetch('/speed' + motor + '?value=' + speed)
                .then(response => console.log("Speed " + motor + " set to " + speed))
                .catch(error => console.error("Error setting speed " + motor + ":", error));
        }
    </script>
</body>
</html>
"""

    
def control_motors(direction):
    if direction == "backward":
        motorA_in1.on()
        motorA_in2.off()
        motorA_ena.duty(speedA)
        
        motorB_in3.on()
        motorB_in4.off()
        motorB_enb.duty(speedB)
        

        
    elif direction == "forward":
        motorA_in1.off()
        motorA_in2.on()
        motorA_ena.duty(speedA)
        
        motorB_in3.off()
        motorB_in4.on()
        motorB_enb.duty(speedB)
        
    
    elif direction == "left":
        motorA_in1.off()
        motorA_in2.off()
        motorA_ena.duty(0)
        
        motorB_in3.on()
        motorB_in4.off()
        motorB_enb.duty(speedB)
        
    
    elif direction == "right":
        motorA_in1.on()
        motorA_in2.off()
        motorA_ena.duty(speedA)
        
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
    global speedA, speedB
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
        elif "GET /speedA" in request:
            speedA = int(request.split("value=")[-1].split(" ")[0])
            motorA_ena.duty(speedA)
        elif "GET /speedB" in request:
            speedB = int(request.split("value=")[-1].split(" ")[0])
            motorB_enb.duty(speedB)
        
        # Respond with the HTML page
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(html)
        cl.close()

# Start the server
serve()




