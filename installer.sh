#!/bin/bash

USERHOME=$HOME

#if [ "$EUID" -ne 0 ]
#  then echo "Please run as root"
#  exit
#fi

APTGET="python3-pip"
PIP="flask waitress bootstrap-flask"

echo "Installing needed applications: $APTGET"
sudo apt-get install $APTGET
echo "Installing needed pip packages: $PIP"
sudo pip install $PIP

while true; do
    read -p "Do you wish to setup the RaspTemp service? [y/n]: " yn
    case $yn in
        [Yy]* ) 
            sed -i -e "s^%MAINFILELOCATION%^$USERHOME/RaspTemp/main.py^g" "$USERHOME/RaspTemp/RaspTemp.service"
            sudo ln -s "$USERHOME/RaspTemp/RaspTemp.service" "/etc/systemd/system/RaspTemp.service"
            break
        ;;
        [Nn]* )
            break
        ;;
        * ) 
            echo "Please answer yes or no."
        ;;
    esac
done

while true; do
    read -p "Do you wish to setup the FreeDNS? [y/n]: " yn
    case $yn in
        [Yy]* ) 
            INSTALLFREEDNS=true
            break
        ;;
        [Nn]* )
            break
        ;;
        * ) 
            echo "Please answer yes or no."
        ;;
    esac
done

if $INSTALLFREEDNS
then
    while true; do
        read -p "FreeDNS domain name (enter to skip)?: " answer
        case $answer in
            "" ) 
                echo "Skipped, please change ""freedns.py"" manually"
                break
            ;;
            * ) 
                sed -i -e "s/%DOMAINNAMETOBEREPLACED%/$answer/g" "$USERHOME/RaspTemp/freedns.py"
                break
            ;;
        esac
    done
    while true; do
        read -p "FreeDNS key (enter to skip)?: " answer
        case $answer in
            "" ) 
                echo "Skipped, please change 'freedns.py' manually"
                break
            ;;
            * ) 
                sed -i -e "s/%KEYTOBEREPLACED%/$answer/g" "$USERHOME/RaspTemp/freedns.py"
                break
            ;;
        esac
    done
    while true; do
        read -p "Do you wish to setup the Crontab for FreeDNS? [y/n]: " yn
        case $yn in
            [Yy]* ) 
                sudo crontab -l > crontabtemp
                echo "0 * * * * python $USERHOME/RaspTemp/freedns.py" >> crontabtemp
                sudo crontab crontabtemp
                rm crontabtemp
                echo "Crontab configured, running ""$USERHOME/RaspTemp/freedns.py"" every hour"
                break
            ;;
            [Nn]* )
                break
            ;;
            * ) 
                echo "Please answer yes or no."
            ;;
        esac
    done
fi

echo "Installation done!"
