# RaspTemp
This is to set up an newly installed Raspberry Pi OS Lite with a small webpage to display the temperature from a DS18B20.

- Add file named "ssh" on the boot partition, to enable SSH

### Set up new user, remove default
-SSH to it, user "pi" password "raspberry".
```
sudo adduser tempmeasureuser
```
- Set fullname to "TempMeasureUser"
- Set a password
```
groups | sed 's/pi //g' | sed 's/ /,/g' | xargs -I{} sudo usermod -a -G {} tempmeasureuser
```
- Exit
- Connect again with tempmeasureuser
```
sudo deluser --remove-home pi
```
## Install webstuff, with Flask
```
sudo apt-get update

sudo apt-get install python3-pip
sudo pip install flask
sudo nano main.py 
```
Add the stuff
```
sudo chmod +x main.py
mkdir templates
cd templates
nano main.html
wget https://toorshia.github.io/justgage/download/justgage-1.2.2.zip
unzip justgage-1.2.2.zip
mkdir static
cp justgage–1.2.2/*.js static/
```
