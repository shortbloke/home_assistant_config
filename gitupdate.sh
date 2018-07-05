#!/bin/bash

skipcheck=0

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -s|--skipcheck)
        skipcheck=1
        shift
        ;;
        *)
            # unknown option
        ;;
    esac
shift
done

if [ "$skipcheck" = "0" ]; then
	hassio homeassistant check
fi

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
