#include <Servo.h>
// A simple sketch to allow the Arduino to interface with the Raspberry Pi and also control the Motor control shield
// The methodology here is that the sabertooth RC is designed for being connected to an RC receiver. We use the Servo
// library to 'spoof' an RC receiver so that we can control the Arduino with Bluetooth, and output an RC PWM signal to 
// simulate similar output to that of an RC receiver. This tricks the Sabertooth into contorlling the motors as we expect.

Servo ST1, ST2; 

// EXCERPT TAKEN FROM SABERTOOTH:
// We'll name the Sabertooth servo channel objects ST1 and ST2.
// For how to configure the Sabertooth, see the DIP Switch Wizard for
//   http://www.dimensionengineering.com/datasheets/SabertoothDIPWizard/start.htm
// Be sure to select RC Microcontroller Mode for use with this sample.
//
// Connections to make:
//   Arduino Pin 9  ->  Sabertooth S1
//   Arduino Pin 10 ->  Sabertooth S2
//   Arduino GND    ->  Sabertooth 0V
//   Arduino VIN    ->  Sabertooth 5V (OPTIONAL, if you want the Sabertooth to power the Arduino)
//
// Sabertooth accepts servo pulses from 1000 us to 2000 us.
// We need to specify the pulse widths in attach(). 0 degrees will be full reverse, 180 degrees will be
// full forward. Sending a servo command of 90 will stop the motor. Whether the servo pulses control
// the motors individually or control throttle and turning depends on your mixed mode setting.

// Notice these attach() calls. The second and third arguments are important.
// With a single argument, the range is 44 to 141 degrees, with 92 being stopped.
// With all three arguments, we can use 0 to 180 degrees, with 90 being stopped.
// EXCERPT FINISHED

String incomingMessage;
String robotDirection;
String robotBias; 

float ch1_input;
float ch2_input;

unsigned ch1_output = 90;
unsigned ch2_output = 90;

void setup()
{
  Serial.begin(9600);
  ST1.attach( 9, 1000, 2000);
  ST2.attach(10, 1000, 2000);
  ST1.write(90);
  ST2.write(90);
}

void loop()
{
    int power;
    
    if(Serial.available() > 0){

        // Message Handling 
        incomingMessage = Serial.readString();
        Serial.print("Received: ");
        Serial.println(incomingMessage);
        robotDirection = incomingMessage.substring(0,1);
        robotBias = incomingMessage.substring(2);

        // The torque provided to the motors can be viewed as a planar vector. The direction
        // can be either Top, Botton, Left or Right depending on where the joystick is. The 
        // bias is mapped to the output of the Sabertooth controller so that we can normalize
        // the joystick's maximum and minimum ranges to the output of the motor controller.
        if (robotDirection == String("T"))
            ch1_output = map(robotBias.toFloat() * 1000, 0, 1000, 91, 180);

        else if (robotDirection == String("B"))
            ch1_output = map(robotBias.toFloat() * 1000, 0, 1000, 89, 0);

        else if (robotDirection == String("L")) {
            ch2_output = map(robotBias.toFloat() * 1000, 0, 1000, 89, 0);
        }

        else if (robotDirection == String("R")) {
            ch2_output = map(robotBias.toFloat() * 1000, 0, 1000, 91, 180);
        }

        else if (robotDirection == String("S")) {
           ch2_output = 90;
           ch1_output = 90;
        }

        // Send some reporting to the Raspberry Pi which will then pipe it to STDOUT in the
        // Linux environment
        else {
            Serial.print("Error: Invalid header: ");
            Serial.println("robotDirection");       
        }
        
        Serial.print("Direction: " + robotDirection);
        Serial.print("\tBias: " + robotBias);
        
        Serial.print("\tCh1 Output: ");
        Serial.println(ch1_output);
        
        Serial.print("\tCh2 Output: ");
        Serial.println(ch2_output);
    }

    // Always write the output
    ST1.write(ch1_output);
    ST2.write(ch2_output);
}
  
