from bluedot import BlueDot
from signal import pause
from serial.tools import list_ports
import serial
import logging
import threading 
import time

def move(pos):
    if pos.top:
        sendCommand('T,' + str(round(pos.distance, 4)))
    elif pos.bottom:
        sendCommand('B,' + str(round(pos.distance, 4)))
    elif pos.left:
        sendCommand('L,' + str(round(pos.distance, 4)))
    elif pos.right:
        sendCommand('R,' + str(round(pos.distance, 4)))

def stop():
    sendCommand('S')

def sendCommand(command): 
    logger.info('Sent: ' + command)
    return ser.write((command + '\r\n').encode())

def readMessageLoop(ser):
    while True:
        message = ser.readline().decode().rstrip()
        handleMessage(message)

def handleMessage(message):
    logger.debug(message)

logger = logging.getLogger('blade-main')
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

# Create formatter and add to console 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# First find arduino (ACM0 type)
devices = list(list_ports.comports())
arduinoPort = ''
for port in devices: 
    print(port)
    if 'ACM0' in port[1]:
        arduinoPort = port[0]

if not arduinoPort:
    raise serial.SerialException('Cannot find port to connect to')

logger.info('Found device at: ' + arduinoPort)
 
ser = serial.Serial(arduinoPort, 9600)

# Beginng reading Daemon
readThread = threading.Thread(target=readMessageLoop, args=(ser,))
readThread.start()

bd = BlueDot()

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

pause()