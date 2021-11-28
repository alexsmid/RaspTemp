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
- Run the install.sh script

This will install the needed packages, set up the service, setup the FreeDNS script and crontab for the FreeDNS script
The service will be called RaspTemp, controllable from systemctl. It will run from RaspTemp.service (throug a link from /etc/systemd/system/)  
The FreeDNS script will be run by crontab (sudo) every hour, and log to /var/log/freedns  
 
# TODO
- [x] Systemd file
- [x] flask-boostrap
- [x] Get gage to to be show
- [x] Get gage working on mobile
- [ ] Remote internet access with private keys
- [x] DynDNS
- [ ] Get temperature
- [ ] Get last updated date
- [x] Python install script
