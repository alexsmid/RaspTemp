# RaspTemp
This is to set up an newly installed Raspberry Pi OS Lite with a small webpage to display the temperature from a DS18B20.
It uses waiterss, flask, bootstrap-flask and JustGage

JustGage download location:

JustGage 1.5.0: https://github.com/toorshia/justgage/releases/latest/download/justgage.js

Raphael 2.2.0: https://cdnjs.cloudflare.com/ajax/libs/raphael/2.2.0/raphael-min.js

## Instructions

- Add file named "ssh" on the boot partition, to enable SSH

### Set up new user, RaspTemp
- SSH to it, user "pi" password "raspberry".
- Set locale, timezone etc:
```
sudo raspi-config
```
- Add new user
```
sudo adduser rasptemp
```
- Set fullname to "RaspTemp"
- Set a password
- Copy the groups from "pi":
```
groups | sed 's/pi //g' | sed 's/ /,/g' | xargs -I{} sudo usermod -a -G {} rasptemp
```
- Exit/disconnet
- Connect again with RaspTemp
### Install the RaspTemp
- Create a folder for RaspTemp:
```
mkdir RaspTemp
```
- Clone the git repository
- Run the installer.sh script
```
. installer.sh
```
This will install the needed packages, set up the service, setup the FreeDNS script and crontab for the FreeDNS script
The service will be called RaspTemp, controllable from systemctl. It will run RaspTemp.service (through a symlink to /etc/systemd/system/)  
The ReadTemp script will be run by crontab every 10 minutes, and log to $HOME/RaspTemp/temperature.log
The FreeDNS script will be run by crontab every hour, and log to $HOME/RaspTemp/freedns.log
 
 ### Set up the sensor
- Connect the DS18B20 to the Raspberry:  
Red cable to pin 1 (3,3v), black to pin 6 (ground), yellow/data to pin 7 (GPIO 4)  
Make sure there is a 4,7kΩ resistor between data and red  
- Open /boot/config.txt with your favorite text editor
- Add the following line to the bottom of the file (gpiopin=4 is pin 7)
```
dtoverlay=w1-gpio,gpiopin=4
```
- You should also load in the device kernel modules by running the following
```
sudo modprobe w1-gpio
sudo modprobe w1-therm
```
- Check that the modules are loaded:
```
lsmod | grep w1
```
- To load the modules every start:
```
sudo nano /etc/modules
```
- Add the following lines to the bottom of the file
```
w1_gpio
w1_therm
```

# TODO
- [x] Systemd file
- [x] flask-boostrap
- [x] Get gage to to be show
- [x] Get gage working on mobile
- [ ] Remote internet access with private keys
- [x] DynDNS
- [x] FreeDNS script
- [x] FreeDNS crontab
- [x] Script for getting temperature and date
- [x] Schedule script for getting the temperature
- [x] Get temperature
- [x] Get last updated date
- [x] Bash install script
