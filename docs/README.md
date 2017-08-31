# Shortbloke's Home Assistant Configuration Files

This is my currently active set of configuration files for my [Home Assistant](https://home-assistant.io) running on Raspberry Pi.
If you are intested in following my progress be sure ⭐️ Star this repository and check out [my blog](https://www.martinrowan.co.uk).

These configuration files enable intgration with a wide range of systems through the power of Home Assistant.

### Configuration File Status [![Build Status](https://travis-ci.org/shortbloke/home_assistant_config.svg?branch=master)](https://travis-ci.org/shortbloke/home_assistant_config)
Each commit triggers a deployement to the latest home assistant version with Python 3.4. This is done though TravisCI. If this sucessfully passes, then my Pi will update itself with the latest configuration automatically.

![My Home Assistant Default View](images/default_view.jpg)

## Core Hardware of Home Assistant Hub
 - [Raspberry Pi 3 Model B](http://amzn.to/2hI9tyc) - Core control system, running Raspbian.
 - [RFXCOM RFXtrx433E](http://amzn.to/2wFwO63) - Enables RX/TX of 433Mhz signals over a range of protocols.
   - Note: Lots of different protocols in use on 433Mhz which may need to be enabled via a management utility. 433Mhz lacks any real security. If you capture the code you can control the device, as I found out by accidentally controlling a neighbour's plug-in sockets.
 - [Aeotec Z-Stick Gen5 (ZW090)](http://amzn.to/2wrrgwI) - Provides interface to Z-Wave Mesh Network devices.
 - Plus case, Power Supply and MicroSD Card.

## Devices controlled by Home Assistant
The following devices are controlled via my Home Assistant configurations. They may also provide sensors as input.
### Climate Control
| Device | Component | Functionality| Limitations |
| ---| ---| --- | --- |
| [Nest Thermostat (3rd generation)](http://amzn.to/2umTkEp) | [Nest](https://home-assistant.io/components/nest/) & related sub components | Temperature sensors and heating status information along with target temperature being able to be controlled via Home Assistant | <ul><li>Requires setup of a Nest Developer account (free)</li><li>Whilst 3rd gen Nest Thermostat in the UK provides the ability to control the hot water system. This isn't exposed via current implementation in Home Assistant.</li></ul> |

### Power and Lighting control
| Device | Component | Functionality| Limitations |
| ---| ---| --- | --- |
| [Lightwave RF Devices](https://www.lightwaverf.com) <ul><li>Plug in sockets ([JSJSLW321](http://amzn.to/2vN1oys))</li><li>Inline Dimmer module ([JSJSLW831](http://amzn.to/2vLdcjH))</li><li>Smartphone Web Link - Hub ([JSJSLW930](http://amzn.to/2vLbJKq)) (Note: Not needed for Home Assistant Control)</li></ul> | [RFXtrx](https://home-assistant.io/components/rfxtrx/) & related sub components | LightwaveRF devices provide an easy solution for retrofitting automation into existing homes. Many other technologies require for example both Live and Neutral to be present at light switches, which is uncommon for UK installations at least. | <ul><li>One-Way communication, you can not query state to know devices status, nor can you confirm if commands sent were obeyed.</li></ul> |
| [TP-Link HS110 WiFi Smart Plug with energy monitoring](http://amzn.to/2vgQU8Q) | [switch.tplink](https://home-assistant.io/components/switch.tplink/) | WiFi controlled plugin adapter with Energy monitoring. Enabling actions/automation to be triggered based on power usage. Similar to Belkin Wemo. | <ul><li>Nothing significant so far. I now have 3 of these deivices to replace Wemo Insight Plugs. Hoping they last longer.</li></ul> |
| [Sonoff WiFi Relay Modules](http://sonoff.itead.cc/en/) (with modified hardware and firmware) <ul><li>Inline 10A Relay ([Sonoff Switch](http://amzn.to/2xmjjIY))</li><li>Inline 16A Relay with temperature and humidity monitoring ([Sonoff TH16](http://amzn.to/2wiJKm0))</li></ul> | [MQTT Switch](https://home-assistant.io/components/switch.mqtt/) | Simple MQTT enabled wifi relay/switches and sensors at an incredibly low cost. With modifications: <ul><li>Hardware modified by solding headers onto Sonoff board to enable custome firmware updating.</li><li>Custom Firmware to provide simple web configuration and control and MQTT support. Currently using [Sonoff-Tasmota](https://github.com/arendst/Sonoff-Tasmota) additional information  in the [project wiki](https://github.com/arendst/Sonoff-Tasmota/wiki)</li></ul> | <ul><li>Need to open up devices and solder headers to flash custom firmware.</li><li>Need to flash custom firmware via [3.3V FTDI USB-to-Serial Converter/Programmer](http://amzn.to/2xlYJIw) (Be sure to set USB to serial programmer to **3.3V**, it may be 5V by default (mine was) and will likely kill the ESP8266 is you supply it with 5V.)</li><li>Need to setup MQTT Broker on Raspberry Pi. I'm using Mosquitto. [Useful setup video](https://www.youtube.com/watch?v=AsDHEDbyLfg)</li><li>The TH16 Device is CE marked and having compared the design to the original switch, with a fuse and greater separation between High and Low voltage components.<li><li>The Sonoff Basic switch is not CE certified, based onthe [CE Certification](https://www.itead.cc/wiki/File:CE_Certificate_for_Sonoff_Series.pdf) document. Caution should be used with this device.</li></ul> |
| [Flamerite Electric Fire](http://www.flameritefires.com/products/floor-standing-suites/junai.html) | [switch.rfxtrx](https://home-assistant.io/components/switch.rfxtrx/) | Our famerite fire came with a 433Mhz remote control. The RFXCOM 433 Transceiver was able to detect the codes from the remote and allow Home Assistant to send the same codes | |
| [Belkin Wemo Insight Switch, WiFi SmartPlug](http://amzn.to/2vMEtmN) | [Wemo](https://home-assistant.io/components/wemo/) | WiFi controlled plugin adapter with Energy monitoring. Enabling actions/automation to be triggered based on power usage. | <ul><li>Questionable reliability: I've had two now fail with similar symptoms when turning off devices which pull a considerable current, ~18kW. This is significantly less than the 13A/240V rated maximum. I've now removed all Wemo Insight Plugs from my home. It's possible the current load readings from the Wemo were wrong, investigating.</li><li>Setup problems: Early firmware versions had problems with setup, especially in environments with multiple access points.</li><li>No memory of last power state. In the event of a recovery from a power cut, the device connected will remain off.</li></ul> |

### Media Players
| Device | Component | Functionality| Limitations |
| ---| ---| --- | --- |
| [Sonos](http://www.sonos.com) | [mediaplayer.sonos](https://home-assistant.io/components/media_player.sonos/) | Automatic detection of all Sonos Devices. Shows what is playing on each device. Able to control playback. Also able to be integrated with Text to Speech components. | |
| [Plex](http://www.plex.tv) | [mediaplayer.plex](https://home-assistant.io/components/media_player.plex/) | Shows activity of Plex Clients. | |
| [Samsung Smart TVs](http://www.samsung.com/uk/tvs/all-tvs/) | [mediaplayer.samsungtv](https://home-assistant.io/components/media_player.samsungtv/) | Discovery component will automatically detect TVs, report status and can be controlled via component. | <ul><li>Not all Smart TV models are fully supported.</li></ul> |
| [Apple TV](https://www.apple.com/uk/tv/) | [Apple_tv](https://home-assistant.io/components/apple_tv/) & related sub components | (Only tested personally tested with Gen3 version) Shows what is playing on AppleTV with device controls. Plus provides access to a remote control. | |

## Sensors providing data to Home Assistant (input only)
### Voice Control 
| Device | Component | Functionality| Limitations |
| ---| ---| --- | --- |
| [Amazon Echo Dot (2nd Generation)](http://amzn.to/2unxhgz) | [Emulated Hue](https://home-assistant.io/components/emulated_hue/) | Voice control input to Home Assistant | |Voice control input to Home Assistant

### Hardware sensors
| Device | Component | Functionality| Limitations |
| ---| ---| --- | --- |
| [Nest Protect (2nd generation) Smoke and Carbon monoxide detectors](http://amzn.to/2wFGOw4) | [Nest](https://home-assistant.io/components/nest/) & related sub components | Monitoring of Smoke and CO2 alarms and system health. | <ul><li>Requires setup of a Nest Developer account (free)</li></ul> | 
| Z-Wave: [Aeotec Multisensor 6 (ZW100)](http://amzn.to/2vkpCNo) | [z-wave](https://home-assistant.io/components/zwave/) plus sub components | A range of movement, light, temperature, humidity sensors in a single device. Has battery or USB power options. Note that when  USB powered device acts as a Z-Wave repeater in the mesh. | <ul><li>Setup may take multiple attempts. Watch [BRUH Z-Wave Video](https://www.youtube.com/watch?v=ajklDCaOGwY) to learn before attempting setup</li></ul> |
| Z-Wave: [Fibaro Gen 5 Multisensor (FGMS-001-ZW5-UK)](http://amzn.to/2wrJK0g) | [z-wave](https://home-assistant.io/components/zwave/) plus sub components | A range of movement, light and temperature sensors in a single battery powered device. | <ul><li>Setup may take multiple attempts. Watch [BRUH Z-Wave Video](https://www.youtube.com/watch?v=ajklDCaOGwY) to learn before attempting setup.</li><li>No humidity sensor</li><li>Battery only, which means it goes to sleep a lot to save power. Currently testing in parallel to see if that really matters</li></ul> |
| Other 433Mhz devices | [RfxTrx](https://home-assistant.io/components/rfxtrx/) | <ul><li>Owl Energy Monitor (investigating)</li><li>Internal Temperature and Humidity monitors [WH5](http://www.ebay.co.uk/itm/Extra-Sensor-for-Weather-Station-with-temp-humidity-f-cast-base-Baro-press/261788376051)</li><ul><li>Temperature readings from WH5 are 40 DegC higher than they should be. This can be corrected by use of a template i.e. `value_template: '{{ (states.sensor.temp_humid_1_temperature.attributes["Temperature"] | float - 40) | round(1) }}'`</li><li>Research page: [Glen Pitt-Pladdy Blog](https://www.pitt-pladdy.com/blog/_20131228-233456_0000_Imagintronix_Temperature_Humidity_Sensor_Protocol_WH15B_for_WH1400_/)</li></ul><li>External Temperature and Humidity sensor, Oregon THGN132N | |
| HP ILO sensor information | [HP_ilo](https://home-assistant.io/components/sensor.hp_ilo/) | Sensor information for HP Servers with ILO such as overall health, temperature at specific points in the chassis | |

### Software sensors
| Component | Provides | Limitations |
| --- | --- | --- |
| [Sun](https://home-assistant.io/components/sun/) | Sun position, enabling automation to be triggered, e.g. at dusk and dawn | |
| [Moon](https://home-assistant.io/components/sensor.moon/) | Phase of the moon | |
| [System Monitor](https://home-assistant.io/components/sensor.systemmonitor/) | System resource usage information on the host system Home Assistant is running on | |
| [Home Assistant SSL Certificate Expiry Checking](https://home-assistant.io/docs/ecosystem/certificates/lets_encrypt/#7---set-up-a-sensor-to-monitor-the-expiry-date-of-the-certificate) | A sensor to show the number of days until the current SSL certificate in use expires. A reminder to renew before it expires | |
| iOS App [Home Assistant App](https://itunes.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401) | With Home Assistant addon [ios](https://home-assistant.io/docs/ecosystem/ios/) enables location tracking plus complete control of HASS, iPhone battery monitoring and is able to receive notifications from Home Assistant | |
 
# Automation Scripts
 - Turning on lights an hour before sunset
 - Turning off power sockets if no movement detected for 30 mins and sockets drawing more than just standby power levels. Triggers notification when sockets are turned off
 - Send notification when Let's Encrypt SSL certificate used for HomeAssistant has less than 3 weeks left before expiry
 - Automatically syncs down changes from github on sucessful travisCI build and restarts Home Assistant
 - Sends notification when disk space or memory are low on RPi or load level is high.

# Additional Info
Private information is stored in secrets.yaml (not uploaded)

# Config updating and validation
 - Changes to configuration are pushed to git using `gitupdate.sh` script.
 - TravisCI is connected to this repository, which will run a script validation for each check-in automatically. Setup as per: https://home-assistant.io/docs/ecosystem/backup/backup_github/
   - Note in order for Travis to work a number of extra files are required:
     - `travis/travis_secrets.yaml` - Contains dummy values for the secrets used in the configuration files
     - `travis/travis.fake_ssl_key` and `travis.fake_ssl_crt` - Are dummy files needed for a Home Assistant configuration setup to use SSL.
 - A successful Travis build triggers a git pull request to update the current configuration, followed by restarting the home assistant service. Enabling changes to be made away from the the Pi/HASS Hub, uploaded to GitHub and directly applied to the running system.

# Backups
I've implemented a simple backup plan which uses a windows file share on my Microserver to backup my Home Automation system. It provides:
 - Weekly and Monthly full SD card backups
 - Daily and Weekly HASS MySQL Database backups
 - Daily and Weekly backup of .homeassistant directory, which contains running config and dependancies.
This is driven my crontab. For more information [read these notes](https://github.com/shortbloke/home_assistant_config/issues/3)
