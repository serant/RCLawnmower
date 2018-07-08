from bluedot import BlueDot
from signal import pause
from serial.tools import list_ports
import serial
import logging
import threading 

def move(pos):
    if pos.top:
        sendCommand('T,' + str(pos.distance))
    elif pos.bottom:
        sendCommand('B,' + str(pos.distance))
    elif pos.left:
        sendCommand('L,' + str(pos.distance))
    elif pos.right:
        sendCommand('R,' + str(pos.distance))

def stop():
    sendCommand('S')

def sendCommand(command): 
    logger.info('Sent: ' + command)
    return ser.write((command + '\r\n').encode())

def readMessageLoop(ser):
    while True:
        message = ser.readline().decode()
        handleMessage(message)

def handleMessage(message):
    logger.debug(message)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
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

bd = BlueDot()

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

pause()