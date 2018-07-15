from bluedot import BlueDot
from signal import pause
from serial.tools import list_ports
import serial
import logging
import threading 

class RoverControl(object):
    def __init__(self):
        self.previousInput = { 'T': 0, 'B': 0, 'L': 0, 'R': 0, }
        self.__initalizeLogging()
        self.__initBlueDot()
        pause()

    def move(self, position):
        distance = round(position.distance, 4)
        if position.top and abs(distance - self.previousInput['T']) >= 0.1:
            self.previousInput['T'] = distance
            return self.__sendCommand('T,' + str(distance))

        elif position.bottom and abs(distance - self.previousInput['B']) >= 0.1:
            self.previousInput['B'] = distance
            return self.__sendCommand('B,' + str(distance))

        elif position.left and abs(distance - self.previousInput['L']) >= 0.1:
            self.previousInput['L'] = distance
            return self.__sendCommand('L,' + str(distance))
        
        elif position.right and abs(distance - self.previousInput['R']) >= 0.1:
            self.previousInput['R'] = distance
            return self.__sendCommand('R,' + str(distance))

    def stop(self):
        return self.__sendCommand('S')

    def __initalizeLogging(self):
        self.logger = logging.getLogger('RoverControl')
        self.logger.setLevel(logging.DEBUG)

        # Create console handler and set level to debug
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)

        # Create formatter and add to console 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console.setFormatter(formatter)
        self.logger.addHandler(self.console)

    # COMMUNICATION
    def __sendCommand(self, command):
        self.logger.info('Sent: ' + command)
        return self.ser.write((command + '\r\n').encode())

    def __initBlueDot(self):
        self.bd = BlueDot()
        self.bd.when_pressed = self.move
        self.bd.when_moved = self.move
        self.bd.when_released = self.stop


    def __findArduinoPort(self):
        devices = list(list_ports.comports())
        arduinoPort = ''
        for port in devices: 
            print(port)
            if 'ACM' in port[1]:
                arduinoPort = port[0]

        if not arduinoPort:
            raise serial.SerialException('Cannot find port to connect to')

        self.logger.info('Found device at: ' + arduinoPort)
        return arduinoPort

    def __initReadMessageLoop(self):
        arduinoPort = self.__findArduinoPort()
        self.ser = serial.Serial(arduinoPort, 9600)
        # Beginng reading Daemon
        self.readThread = threading.Thread(target=self.readMessageLoop, args=(self.ser,))
        self.readThread.start()

    def readMessageLoop(self, ser):
        while True:
            message = ser.readline().decode().rstrip()
            self.__handleMessage(message)

    def __handleMessage(self, message):
        self.logger.debug(message)
        return
