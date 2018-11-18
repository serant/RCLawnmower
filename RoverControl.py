from bluedot import BlueDot
from signal import pause
from serial.tools import list_ports
import serial
import logging
import threading 

class RoverControl(object):
    """
    The Rover Control class provides an interface from the Bluedot app on an Android smartphone to 
    the Remote Controlled Robotic Lawnmower. This class achieves this by providing two roles:

    1. Listens for a bluetooth connection to the Bluedot app through a Raspberry Pi or Debian based
        linux device

    2. Establishes a serial connection between the Raspberry Pi and an Arduino through USB. As commands are 
        read in throubh the Bluedot connection, they are sent to the Arduino through the serial connection.

    The RoverControl class also executes a message handling loop where incoming messages from the Arduino are 
    redirected to STDOUT on the Raspberry Pi. This operates in a seperate loop.

    Supplementary Information
        * The serial connection is protected within the class by a Sempahore bound to a single connection 
            (i.e. additional messages will be placed in a queue on a FIFO basis)
    """
    def __init__(self):
        self.previousPosition = {}
        self.__initLogging()
        self.__initReadMessageLoop()
        self.__initBlueDot()
        pause()

    def move(self, distance, direction) -> str:
        """
        Send a command to the Arduino Uno in the robotic lawnmower to move in a particular direciton. Directions
        are currently one of the following:
            * T -> Top
            * B -> Bottom
            * L -> Left
            * R -> Right

        :param:distance A normalized float between 0 and 1 denoting how much torque the motors should provide in 
            the vector drawn by the position
        :param:direction One of the aforementioned Directions as a character

        Returns:
            The resulting serial response as a str
        """
        return self.__sendCommand(direction + ',' + str(distance))

    def stop(self, pos) -> str:
        """
        Provides an emergency stop feature by sending 'S' the Arduino which denotes stop

        Returns:
            The resulting serial response as a str 
        """
        return self.__sendCommand('S')

    def __bdMove(self, position):
        """
        Interprets the location of the joystick in Bluedot as a command to send to the Arduino

        :param:position is a Bluedot required parameter which is a struct containing the direction and normalized
            position of the joystick

        Supplementary Information:
            * Ensures that a command is only send to the Arduino if the latest instruction from the joystick exceeds
                a certain threshold value to ensure that the Arduino is not oversaturated with incoming instructions
        """
        direction = 0
        distance = round(position.distance, 4)

        # Determine direction from BD position
        if   position.top:      direction = 'T'
        elif position.bottom:   direction = 'B'
        elif position.left:     direction = 'L'
        elif position.right:    direction = 'R'

        # Return if change in distance is less than 0.1 in the same direction
        if direction == self.previousPosition['direction'] and \
            abs(distance - self.previousPosition) <= 0.1: return

        self.previousPosition['direction'] = direction
        self.previousPosition['distance'] = distance
        self.move(distance, direction)

    def __initLogging(self):
        """
        Creates a formatted log stream which is piped to STDOUT on the Raspberry Pi
        """
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
    def __sendCommand(self, command) -> str:
        """
        Sends a serial raw formatted command to the Arduino. :meth:__sendCommand formats the 
        command as a raw formatted string suffixed with a CRLF line ending

        :param:command is a string to send 

        Returns:
            The result of the serial communicate to the board as a str
        """
        self.logger.info('Sent: ' + command)
        return self.ser.write((command + '\r\n').encode())

    def __initBlueDot(self):
        """
        Instantiates and initializes the Bluedot object which looks for a paired device and listens
        for commands sent from the joystick
        """
        self.bd = BlueDot()
        self.bd.when_pressed = self.__bdMove
        self.bd.when_moved = self.__bdMove
        self.bd.when_released = self.stop


    def __findArduinoPort(self) -> str:
        """
        Automatically looks for the port to connect to an Arduino device.

        Returns:
            The port value that was found
        """
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
        """
        Starts a daemonized process that connects to the Arduino from the Raspberry Pi and begins
        piping messages from the Arduino to STDOUT
        """
        arduinoPort = self.__findArduinoPort()
        self.ser = serial.Serial(arduinoPort, 9600)
        # Beginng reading Daemon
        self.readThread = threading.Thread(target=self.__readMessageLoop, args=(self.ser,))
        self.readThread.start()

    def __readMessageLoop(self, ser):
        """
        The main process for the serial readLoop from the Raspberry Pi to the Arduino

        :param:ser is the Serial object that the connection to the Arduino is established through
        """
        while True:
            message = ser.readline().decode().rstrip()
            self.__handleMessage(message)

    def __handleMessage(self, message):
        """
        Pipes a message to the logger

        :param:message is the message to pip to the logger
        """
        self.logger.debug(message)
        return
