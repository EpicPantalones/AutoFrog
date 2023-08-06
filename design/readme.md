# Project Overview
## Original Request
"Two cages, with misters, lights and fans, all running off 120V AC power. All devices need to be controlled by a single controller. Devices will need to be turned on/off at reprogrammable times of day, with multiple on/off times per device. Programs need to be programmable down to 1-sec intervals. Will need to track time of day, so that programs run at the same times. Need to be able to have different programs for all devices, and every day of the week. Need to be able to measure humidity and use the humidity to control the fans, based on a user set threshold. want the ability to recover from power loss and update time of day and put lights back into the state they were prior to power loss. Misters should ALWAYS start in the OFF state after power loss and NOT return to on, if they were running when power goes out. Would like a webpage to set the config file if possible, but need a way to modify programs as applicable. would be nice if RTC autochanged with daylight savings time and autosynced to remove clock drift. electric power needs to be in a box that protects any circuitry from being contacted inadvertantly."
### Device channels (by cage)
2 lights \
1 mister \
1 fan

## Electrical block diagram
![Block Diagram](BlockDiagram.png)
System has one AC input and one input on the logic bus. Has six AC channel outputs, which will vary in size depending on requirement, as well as two 12v outputs and 1 logic bus for humidity sensing. Note that for simplicity, the earth ground is omitted, and the neutral wires all connect to the same line regardless of voltage.
### Design
The power is inputted directly from 120v AC through a C13 connector with a protective fuse. This also has the master power switch. From there the power is split into two branches. The first is the AC line that goes directly to six of the eight channels on the relay, for the six AC outputs. The second branch goes to a 12v converter, which in turn produces two branches of 12v DC power: one for powering the two 12v channels, and one that is further downconverted to a 5v supply for the raspberry pi and the logical power input of the relay. The raspberry Pi's logical output is 3.3v, so there is a small level converter for the 5v required on the relay. The ground to the LC comes from the Rpi, and Va and Vb are supply by directly wiring to their respective supplies. The raspberry Pi also sends a wire out to the outside which allows the humidity sensor to send data back.

## Mechanical Design
We purchased a small clear box to contain all the circuitry. Due to time constraints, the harnessing and box are a bit rushed, but the box provides ample protection and does a good job supporting both the standoffs for the circuitry and the output connectors. Also due to the time contraints, there was not enough time to measure all of the wires, so the harnessing is not nearly as neat as I would like it to be. Next time, I would do a better job of designing the wiring layout before beginning execution of the build phase.

## Materials List:
The full list of items purchase is on amazon, link here: \
https://www.amazon.com/hz/wishlist/ls/33Y2IXWOOTIRV/ref=nav_wishlist_lists_3

### Items
- **Raspberry Pi Zero W**: the brains.
- **MicroSD card**: minimum 16GB. houses OS for Rpi
- **AZDelivery Humidity Sensor**: measures humidity in the cages to control fan speed.
- **12v DC Power Supply**: Modified standard 12v power supply. Removed the AC type A connector and barrel plug output and used just the bare wiring.
- **5v DC Converter**: downconverts the 12V line for Rpi and humidity sensors.
- **Sunfounder 8 Chn Relay**: Takes in AC or DC power and acts as a digitally controlled switch. Logical is controlled on a 5v level, which must be powered seperately from the host device.
- **HiSense Logic Level Convertor**: converts the logic level of the Rpi (3.3v) to the level of the relay (5v).
- **3Dman 15 Rocker Connector**: Used as system input, a C13 connector with a 5A fuse and a rocker switch. Fuse can be swapped for 10A if necessary.
- **Panel mount AC outlets**: Used as the channel outputs for the 6 AC channels.
- **BTF-Lightning connectors**: 2 pin version used as the connections for the 12v channels and the 3 pin version used to connect to the humidity sensor. In reality I should have gotten 2 connectors for 2 voltages, but it was a tactical decision...
- **Various Types of Wire, Standoffs, Suction Cups**

## Software Design
### Overview
Using the userend GUI, users can create and assign channels and configurations remotely from their machine. Upon confirmation, the GUI sends those configurations to the Rpi Zero, which receives them and immediately loads them into the system. The Rpi Zero has a default state in the event of power loss, and will automatically come online and begin listening again after rebooting. Users can also change the state of the channels manually, which persists until the next event in the current config file. There may be any number of configuration files, and not all configuration files are required to be assigned to a channel. Channels may share a configuration.
### User End
User Gui was designed with Tkinter, and has two main modes: configuration mode, and live command mode. In configuration mode, users may add, remove, or edit files to create custom times for the channels to be considered ON or OFF. in Live command mode, users can see the active status of the channels and can send commands to change the state of channels.
### Server
The server end uses threads to listen for commands and other than that controls some global variables that are used to determine the configuration of the system. The server controls the channels down to the second level, but it should also be noted that the inputs can only come at the minute level.