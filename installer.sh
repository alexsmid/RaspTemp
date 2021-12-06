#!/bin/bash

APTGET="python3-pip"
PIP="flask waitress bootstrap-flask livereload"

echo "Installing needed applications: $APTGET"
sudo apt-get install $APTGET
echo "Installing needed pip packages: $PIP"
sudo pip install $PIP

while true; do
    read -p "Do you wish to change the title of the web page? (default title: Temperature) [enter to skip]: " answer
    case $answer in
        "" ) 
            echo "Skipped, please change ""templates/main.html"" manually"
            break
        ;;
        * ) 
            sed -i -e "s^<title>Temperature</title>^<title>$answer</title>^g" "$HOME/RaspTemp/templates/main.html"
            sed -i -e "s^%TEMPERATUREFILELOCATION%^$HOME/RaspTemp/temperature.log^g" "$HOME/RaspTemp/main.py"
            break
        ;;
    esac
done

while true; do
    read -p "Do you wish to setup the RaspTemp service? [y/n]: " yn
    case $yn in
        [Yy]* ) 
            sed -i -e "s^%MAINFILELOCATION%^$HOME/RaspTemp/main.py^g" "$HOME/RaspTemp/RaspTemp.service"
            sudo ln -s "$HOME/RaspTemp/RaspTemp.service" "/etc/systemd/system/RaspTemp.service"
            sudo systemctl enable RaspTemp
            break
        ;;
        [Nn]* )
            break
        ;;
        * ) 
            echo "Please answer ""Y/y"" or ""N/n""."
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
            INSTALLFREEDNS=false
            break
        ;;
        * ) 
            echo "Please answer ""Y/y"" or ""N/n""."
        ;;
    esac
done

if $INSTALLFREEDNS
then
    while true; do
        read -p "FreeDNS domain name? [enter to skip]: " answer
        case $answer in
            "" ) 
                echo "Skipped, please change ""freedns.py"" manually"
                break
            ;;
            * ) 
                sed -i -e "s/%DOMAINNAMETOBEREPLACED%/$answer/g" "$HOME/RaspTemp/freedns.py"
                break
            ;;
        esac
    done
    while true; do
        read -p "FreeDNS key? [enter to skip]: " answer
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
        read -p "Do you wish to setup the Crontab for FreeDNS? [y/n]: " yn
        case $yn in
            [Yy]* ) 
                crontab -l > crontabtemp
                echo "0 * * * * python $HOME/RaspTemp/freedns.py" >> crontabtemp
                crontab crontabtemp
                rm crontabtemp
                echo "Crontab configured, running ""$HOME/RaspTemp/freedns.py"" every hour"
                break
            ;;
            [Nn]* )
                break
            ;;
            * ) 
                echo "Please answer ""Y/y"" or ""N/n""."
            ;;
        esac
    done
fi

echo "Installation done!"
