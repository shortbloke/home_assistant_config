#!/bin/bash

cd /home/hass/.homeassistant
source /srv/hass/hass_venv/bin/activate
hass --script check_config

while true; do
    read -p "All OK? Add files to Git? (y/n)" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

git add .
git status
echo -n "Enter the Description for the Change: " [Minor Update]
read CHANGE_MSG
git commit -m "${CHANGE_MSG}"
git push origin master

exit
