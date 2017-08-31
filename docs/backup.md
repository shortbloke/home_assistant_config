# Backups
I've implemented a simple backup plan which uses a windows file share on my Microserver to backup my Home Automation system. It provides:
 - Weekly and Monthly full SD card backups
 - Daily and Weekly HASS MySQL Database backups
 - Daily and Weekly backup of .homeassistant directory, which contains running config and dependancies.
This is driven my crontab. For more information [read these notes](https://github.com/shortbloke/home_assistant_config/issues/3)