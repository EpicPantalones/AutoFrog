## Project Overview
## Original Request
"Two cages, with misters, lights and fans, all running off 120V AC power. All devices need to be controlled by a single controller. Devices will need to be turned on/off at reprogrammable times of day, with multiple on/off times per device. Programs need to be programmable down to 1-sec intervals. Will need to track time of day, so that programs run at the same times. Need to be able to have different programs for all devices, and every day of the week. Need to be able to measure humidity and use the humidity to control the fans, based on a user set threshold. want the ability to recover from power loss and update time of day and put lights back into the state they were prior to power loss. Misters should ALWAYS start in the OFF state after power loss and NOT return to on, if they were running when power goes out. Would like a webpage to set the config file if possible, but need a way to modify programs as applicable. would be nice if RTC autochanged with daylight savings time and autosynced to remove clock drift. electric power needs to be in a box that protects any circuitry from being contacted inadvertantly."
### Device channels (by cage)
2 lights \
1 mister \
1 fan

# Electrical block diagram
![Block Diagram](BlockDiagram.png)
System has one AC input and one input on the logic bus. Has six AC channel outputs, which will vary in size depending on requirement, as well as two 12v outputs and 1 logic bus for humidity sensing. \
**AC POWER:** AC power is received externally from the female AC plug. AC power is split amongst the six channels output and one branch to a 120vAC to 12vDC converter. AC outputs are also in standard plug form. \
**12v DC POWER:** 12vDC power is output from the converter and split into the two 12v channels, each output as a 2-pin BTF-Lightning, as well as a branch for the 12vDC to 5vDC converter. \
**5v DC POWER:** 5vDC is output from the converter and used to power the logic element of the relay, the Rpi Zero, as well as ouputting on the 3-pin BTF-Lightning to power and receive data for the humidity sensors.

# Mechanical Design
Hopefully this will all be able to fit in a relatively small box. I would like to get it 3D printed, and so I will try to compact everything such that it will fit within the bounds of a printer. The box itself can be very simple, and from there I just add some holes for the various inputs and outputs, as well as a removable lid of some sort. Will post 3d sketchs when parts list is more narrowed down.

## Materials List:
The full list of items purchase is on amazon, link here: \
https://www.amazon.com/hz/wishlist/ls/33Y2IXWOOTIRV/ref=nav_wishlist_lists_3

### Items
- **Rasberry Pi Zero W**: the brains.
- **MicroSD card**: minimum 16GB. houses OS for Rpi
- **AZDelivery Humidity Sensor**: measures humidity in the cages to control fan speed.
- **12v Power Supply**: takes AC power and converts for the fans and logical systems.
- **12v to 5v Converter**: down-converts the 12V line for Rpi and humidity sensors.
- **Sunfounder 8 Chn Relay**: Takes in AC or DC power and acts as a digitally controlled switch.
- **GearIT 16 Gauge Wire**: Used on the AC systems for safety.
- **20 Gauge 3 conductor wire**: Used to connect the fans and the humidity sensors, since it provides ample weather protection from wet environments.
- **20 Gauge standard wire**: Used internally to connect elements.
- **3Dman 15 Rocker**: Used as system input, has a 5A fuse and a rocker switch. Fuse can be swapped for 10A if necessary.
- **Panel mount AC outlets**: Used as the channel outputs for the 6 AC channels. Positive from the relays, neutral and ground go to the rocker input. 
- **BTF-Lightning connectors**: Used as the connections for the 2 fan channels and the connections to the humidity sensors in combination with the 3 conductor wire. There are TWO types of BTF connectors: 2-pin for the fans, and 3-pin for the sensors. The disctinction is important because they do NOT run at the same voltages.
- **Standoffs, Suction Cups**: Mechanical. Standoffs for circuitry, and suction cups for the humidity sensors to stick to the glass and stay in place.

# Software Design
## Overview
Using the userend GUI, users will be able to create and assign channels and configurations remotely from their machine. Upon confirmation, the GUI will send those configurations to the Rpi Zero, which will receive them and immediately load them into the system. The Rpi Zero will have a default state in the event of power loss, and will be able to automatically come online and begin listening again after rebooting. Users will also be able to change the state of the channels manually, which will persist until the next event in the current config file. There may be any number of configuration files, and not all configuration files are required to have a persistant channel. Channels may share a configuration.
### System Requirements
- User can create, edit, assign, and remove configuration files.
- User can manually control the state of a given channel.
- User can change the fan config according to certain presets.
- Rpi can boot and beginning running on its own in a repeatable manner.
- Rpi can maintain a RTC accurate to daylight savings time.
- The Rpi has a static IP on the network to ensure socket compatibility after power loss.
- If possible, RPi leaves room for available GPIO to be used in the future.
## System Architecture
### User End

### Server
**Overview** \
The rasberry pi server will have a folder for receiving files transferred to it using the SCP function in the user end (see above). While the server is running, the following tasks should be running concurrently:
- Checking to see if the current time correclates to any config triggers.
- Checking if it has received new configuration (see below, Receiving Configurations)
- Listening for commands to manually change the system configuration. \
**Receiving Configurations** \
The system should be running in the current working directory of the server (meaning that ./ is Autofrog/server/). When ./received has files in it and are ready to be handled, the client sends a message (exact structure TBD). After receiving that message, the Rpi should copy all the files into the configs folder using "cp", which will handle both edits and additions. Finally, the client will have sent a file called "manifest.txt" which contains a list of the 8 channel's desired config files, the defaults if they have changed, and any files to be deleted from the system. These should all be handled appropriately. Finally, the Rasberry Pi will reload the configurations of each channel. This should not affect the current state of the system.
**Listening For Commands**
The Rpi should have a socket connection that listens for commands to perform. Commands will come in the form (??? TBD ???) which indicates what the Rpi should do. 
**Config Triggers**
Each channel has an assigned config file, which is a list of times and actions. Whenver one of those times occurs, the channel should change accordingly.