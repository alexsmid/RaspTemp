#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

APTGET="python3-pip"
PIP="flask waitress bootstrap-flask"

Echo "Installing needed applications: $APTGET"
sudo apt-get install $APTGET
Echo "Installing needed pip packages: $PIP"
sudo pip install $PIP

while true; do
    read -p "Do you wish to setup the RaspTemp service?: " yn
    case $yn in
        [Yy]* ) 
            sudo ln -s "$HOME/RaspTemp/RaspTemp.service" RaspTemp.service
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
    read -p "Do you wish to setup the FreeDNS?: " yn
    case $yn in
        [Yy]* ) 
            INSTALLFREEDNS= true
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

if [$INSTALLFREEDNS]
then
    while true; do
        read -p "FreeDNS domain name (enter to skip): " answer
        case $answer in
            "" ) 
                echo "Skipped, please change 'freedns.py' manually"
                break
            ;;
            * ) 
                sed -i -e "s/%DOMAINNAMETOBEREPLACED%/$answer/g" "$HOME/RaspTemp/freedns.py"
                break
            ;;
        esac
    done
    while true; do
        read -p "FreeDNS key (enter to skip): " answer
        case $answer in
            "" ) 
                echo "Skipped, please change 'freedns.py' manually"
                break
            ;;
            * ) 
                sed -i -e "s/%KEYTOBEREPLACED%/$answer/g" "$HOME/RaspTemp/freedns.py"
                break
            ;;
        esac
    done
    while true; do
        read -p "Do you wish to setup the Crontab for FreeDNS?: " yn
        case $yn in
            [Yy]* ) 
                sudo crontab -l > crontabtemp
                echo "0 * * * * sudo python $HOME/RaspTemp/freedns.py" >> crontabtemp
                crontab crontabtemp
                rm crontabtemp
                echo "Crontab configured, running ""$HOME/RaspTemp/freedns.py"" every hour"
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
