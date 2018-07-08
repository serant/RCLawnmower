from bluedot import BlueDot
from signal import pause
from serial.tools import list_ports
import serial

# First find arduino (ACM0 type)
devices = list(list_ports.comports())
arduinoPort = ''
for port in devices: 
    if 'ACM0' in port[1]:
        arduinoPort = port[0]
        

print(arduinoPort)

ser = serial.Serial(arduinoPort, 9600)
while True:
    print ser.readline()

bd = BlueDot()

def move(pos):
    if pos.top:
        print('T,' + pos.distance)
    elif pos.bottom:
        print('B,' + pos.distance)
    elif pos.left:
        print('L,' + pos.distance)
    elif pos.right:
        print('R,' + pos.distance)

def stop():
    print('S,')

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

pause()