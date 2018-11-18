# Electric RC Lawnmower

The firmware for an RC electric lawnmower designed to provide lawn care service to customers with challenging property terrains. The project features of this device include:
  * Rear wheel drive with high torque motors
  * Bluetooth control from a smartphone using the [Blue Dot App](https://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot&hl=en_CA) for Android or through a 2 Channel RC controller
  * Fully electric powertrain and cutting functionality
  * Removable lithium battery which provides 45 minutes of runtime
  * Fast charge capability providing a full charge within one hour
  * Zero-turn functionality using industrial caster wheels

## Getting Started

On  the Raspberry Pi:
```
git clone https://github.com/serant/Autonomous-Lawnmower.git
cd Autonomous-Lawnmower
python3.6 ./main.py
```

## Deployment

#### Software
  * Arduino Uno R3 with the `bladerover/bladerover.ino` sketch uploaded
  * Raspberry Pi 3.X with Rasbian Stretch or later
  * Arduino Uno R3 must be connected to the Raspberry Pi 3.X USB bus
  * Android phone paired through Bluetooth to allow for control through Bluedot

## Built With
* [Blue Dot App](https://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot&hl=en_CA) - Used as a Bluetooth remote
* [Raspberry Pi 3]() - Used for main process
* [Arduino Uno R3]() - Used to mock an RC receiver and uses PWM to control the Sabertooth motor controller
* [Sabertooth RC]() - Used to control two 24V high torque motors

## Authors

* **Seran Thirugnanam** - Product design, engineering
* **Hamza Qureshi** - Product design, marketing 
