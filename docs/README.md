# Shortbloke's Home Assistant Configuration Files [![Build Status](https://travis-ci.org/shortbloke/home_assistant_config.svg?branch=master)](https://travis-ci.org/shortbloke/home_assistant_config)

This is my currently active set of configuration files for my [Home Assistant](https://home-assistant.io) running on Raspberry Pi.
If you are interested in following my progress be sure ⭐️ Star this repository and check out [my blog](https://www.martinrowan.co.uk).

## Configuration File Status

Each commit triggers a deployment to the latest home assistant version with Python 3.6 and 3.7. This is done though TravisCI. If this successfully passes, then my Pi will update itself with the latest configuration automatically.

![My Home Assistant Default View](images/default_view.jpg)

## Configuration Organisation

I've limited the contents of configuration.yaml and utilised [packages](https://www.home-assistant.io/docs/configuration/packages/) to provide some grouping, in order to make it easier to understand and maintain.

Packages provide an simple way to encapsulate all the different configuration elements for a adding support for a given component or device. Rather than needing to update many different files the changes are kept contained in a single file per package.

## Core Hardware of Home Assistant Hub

- [Raspberry Pi 4 Model B 4GB RAM](https://amzn.to/3a4gGQc) - Core control system, running on [Hass.io](https://www.home-assistant.io/hassio/).
- [Raspberry Pi Zero W](https://amzn.to/2ZLhm7d) - Hosting [Xiaomi Mi Flora to MQTT Gateway](https://github.com/ThomDietrich/miflora-mqtt-daemon). Mi Flora Bluetooth LE range was limited, the Pi Zero is positioned nearer the plants, and sends status over WiFi via MQTT.
- [RFXCOM RFXtrx433E](http://www.rfxcom.com/store/Transceivers/14103) - Enables RX/TX of 433Mhz signals over a range of protocols.
  - Note: Lots of different protocols in use on 433Mhz which may need to be enabled via a management utility. 433Mhz lacks any real security, if you capture the code you can control the device, as I found out by accidentally controlling a neighbour's plug-in sockets.
- [Nortek GoControl HUSBZB-1](https://www.nortekcontrol.com/products/2gig/husbzb-1-gocontrol-quickstick-combo/) - Provides support for Zigbee and I had hoped for Z-Wave too, but this doesn't support EU/UK frequencies!

## More Information

- [Devices controlled and sensors monitored](devices.md)
- [Automation and shell scripts](automations.md)
- [Configuration validation and automatic deployment](build_deploy.md)

**Note: Private information is stored in secrets.yaml (not uploaded)**
