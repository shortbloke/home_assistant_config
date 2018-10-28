# Shortbloke's Home Assistant Configuration Files [![Build Status](https://travis-ci.org/shortbloke/home_assistant_config.svg?branch=master)](https://travis-ci.org/shortbloke/home_assistant_config)

This is my currently active set of configuration files for my [Home Assistant](https://home-assistant.io) running on Raspberry Pi.
If you are interested in following my progress be sure ⭐️ Star this repository and check out [my blog](https://www.martinrowan.co.uk).

## Configuration File Status

Each commit triggers a deployment to the latest home assistant version with Python 3.6. This is done though TravisCI. If this successfully passes, then my Pi will update itself with the latest configuration automatically.

![My Home Assistant Default View](images/default_view.jpg)

## Core Hardware of Home Assistant Hub

- [Raspberry Pi 3 Model B+](https://amzn.to/2DabgWG) - Core control system, running on [Hass.io](https://www.home-assistant.io/hassio/).
- [RFXCOM RFXtrx433E](http://www.rfxcom.com/store/Transceivers/14103) - Enables RX/TX of 433Mhz signals over a range of protocols.
  - Note: Lots of different protocols in use on 433Mhz which may need to be enabled via a management utility. 433Mhz lacks any real security, if you capture the code you can control the device, as I found out by accidentally controlling a neighbour's plug-in sockets.
- [Aeotec Z-Stick Gen5 (ZW090)](http://amzn.to/2wrrgwI) - Provides interface to Z-Wave Mesh Network devices.

## More Information

- [Devices controlled and sensors monitored](devices.md)
- [Automation and shell scripts](automations.md)
- [Configuration validation and automatic deployment](build_deploy.md)

**Note: Private information is stored in secrets.yaml (not uploaded)**
