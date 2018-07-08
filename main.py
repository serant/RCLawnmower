from bluedot import BlueDot
from signal import pause
from serial.tools import list_ports
import serial
import logging
import threading 

# First find arduino (ACM0 type)
devices = list(list_ports.comports())
arduinoPort = ''
for port in devices: 
    print(port)
    if 'ACM0' in port[1]:
        arduinoPort = port[0]

if not arduinoPort:
    raise serial.SerialException('Cannot find port to connect to')

logging.info('Found device at: ' + arduinoPort)
 
ser = serial.Serial(arduinoPort, 9600)

# Beginng reading Daemon
readThread = threading.Thread(target=readMessageLoop, args=(ser,))

bd = BlueDot()

def move(pos):
    if pos.top:
        sendCommand('T,' + pos.distance)
    elif pos.bottom:
        sendCommand('B,' + pos.distance)
    elif pos.left:
        sendCommand('L,' + pos.distance)
    elif pos.right:
        sendCommand('R,' + pos.distance)

def stop():
    sendCommand('S')

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

def sendCommand(command): 
    logging.info('Sent: ' + command)
    return ser.write((command + '\r\n').encode())

def readMessageLoop(ser):
    while True:
        message = ser.readline().decode()
        handleMessage(message)

def handleMessage(message):
    logging.debug(message)

pause()