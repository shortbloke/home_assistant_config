# Shortbloke's Home Assistant Configuration Files [![Build Status](https://travis-ci.org/shortbloke/home_assistant_config.svg?branch=master)](https://travis-ci.org/shortbloke/home_assistant_config)

This is my currently active set of configuration files for my [Home Assistant](https://home-assistant.io) running on Raspberry Pi. Integrating with:

## Core Hardware of Home Assistant Hub
 - [Raspberry Pi 3 Model B](http://amzn.to/2hI9tyc) - Core control system, running Rasbian.
 - [RFXCOM RFXtrx433E](http://amzn.to/2wFwO63) - Enables RX/TX of 433Mhz signals over a range of protcols.
   - Note: Lotds of different protols in use on 433Mhz which may need to be enabled via a management utility. 433Mhz lacks any real security. If you capture the code you can control the device, as I found out by accidentially controlling a neighbours plug-in sockets.
 - [Aeotec Z-Stick Gen5 (ZW090)](http://amzn.to/2wrrgwI) - Provides interface to Z-Wave Mesh Network devices.
 - Plus case, Power Supply and MicroSD Card.

## Devices controlled by Home Assistant
The following devices are controlled via my Home Assisant configurations. They may also provide sensors as input.
 - [Amazon Echo Dot (2nd Generation)](http://amzn.to/2unxhgz)
   - Home Assistant Component: [Emulated Hue](https://home-assistant.io/components/emulated_hue/)
   - Provides: Voice control input to Home Assisant 
 - [Nest Thermostat (3rd generation)](http://amzn.to/2umTkEp)
   - Home Assistant Component: [Nest](https://home-assistant.io/components/nest/) & and related sub components
   - Provides: Temperature sensors and heating status information along with target temperature being able to be controlled via Home Assistant
   - Limitations: 
     - Requires setup of a Nest Developer account (free)
     - Whilst 3rd gen Nest Thermostat in the UK provides the ability to control the hot water system. This isn't exposed via current implementation in Home Assistant.
 ### Power and Lighting control
 - [Lightwave RF Devices](https://www.lightwaverf.com)
   - Current devices in use:
	 - Plug in sockets ([JSJSLW321](http://amzn.to/2vN1oys))
     - Inline Dimmer module ([JSJSLW831](http://amzn.to/2vLdcjH))
     - Smartphone Web Link - Hub ([JSJSLW930](http://amzn.to/2vLbJKq)) (Note: Not needed for Home Assisant Control)
   - Home Assistant Component: [RFXtrx](https://home-assistant.io/components/rfxtrx/)
   - Provides: LightwaveRF devices provide an easy solution for retrofitting automation into existing homes. Many other technologies require for example both Live and Neutral to be present at light switches, which is uncommon for UK installations at least.
   - Limitation: One-Way communication, you can not query state to know devices status, nor can you confirm if commands sent were obeyed.
 - [Belkin Wemo Insight Switch, WiFi SmartPlug](http://amzn.to/2vMEtmN)
   - Home Assistant Component: [Wemo](https://home-assistant.io/components/wemo/)
   - Provides: WiFi controlled plugin adapter with Energy monitoring. Enabling actions/automation to be triggered based on power usage.
   - Limitations: 
     - Questionable reliability: I've had 1 that has died less than a year old.
     - Setup problems: Early firmware versions had problems with setup, especially in environments with multiple access points.
     - No memory of last power state. In the event of a recovery from a power cut, the device connected will remain off. 
 - [TP-Link HS110 WiFi Smart Plug with energy monitoring](http://amzn.to/2vgQU8Q)
   - Home Assistant Component: [switch.tplink](https://home-assistant.io/components/switch.tplink/)
   - Provides: WiFi controlled plugin adapter with Energy monitoring. Enabling actions/automation to be triggered based on power usage. Similar to Belkin Wemo.
   - Limitations: Too early to report.
 - [Flamerite Eletric Fire](http://www.flameritefires.com/products/floor-standing-suites/junai.html)
   - Home Assistant Component: [switch.rfxtrx](https://home-assistant.io/components/switch.rfxtrx/)
   - Provides: Our famerite fire came with a 433Mhz remote control. The RFXCOM 433 Tranceiver was able to dectect the codes from the remote and allow Home Assistant to send the same codes
### Media Players
 - [Sonos](http://www.sonos.com)
   - Home Assistant Component: [mediaplayer.sonos](https://home-assistant.io/components/media_player.sonos/)
   - Provides: Automatic detection of all Sonos Devices. Shows what is playing on each device. Able to control playback. Also able to be integrated with Text to Speech components.
 - [Plex](http://www.plex.tv)
   - Home Assistant Component: [mediaplayer.plex](https://home-assistant.io/components/media_player.plex/)
   - Provides: Shows activity of Plex Clients.
 - [Samsung Smart TVs](http://www.samsung.com/uk/tvs/all-tvs/)
   - Home Assistant Component: [mediaplayer.samsungtv](https://home-assistant.io/components/media_player.samsungtv/)
   - Provides: Discovery component will automatically detect TVs, report status and can be controlled via component.
   - Limitations: Not all Smart TV models are fully supported.
 - [Apple TV](https://www.apple.com/uk/tv/)
  - Home Assistant Component: [Apple_tv](https://home-assistant.io/components/apple_tv/)
  - Provides: (Only tested personally tested with Gen3 version) Shows what is playing on AppleTV with device controls.

## Sensors providing data to Home Assistant (input only)
### Hardware sensors
 - [Nest Protect (2nd generation) Smoke and Carbon monoxide detectors](http://amzn.to/2wFGOw4)
   - Home Assistant Component: [Nest](https://home-assistant.io/components/nest/) and related sub components
   - Provides: Monitoring of Smoke and CO2 alarms and system health.
   - Limitations: Requires setup of a Nest Developer account (free)
 - Z-Wave Devices:
   - [Aeotec Multisensor 6 (ZW100)](http://amzn.to/2vkpCNo)
     - Home Assistant Component: [z-wave](https://home-assistant.io/components/zwave/) plus sub components
     - Provides: A range of movement, light, temperature, humidity sensors in a single device. Has battery or USB power options. Note that when  USB powered device acts as a Z-Wave repeater in the mesh.
     - Limitations:
       - Setup may take multiple attempts. Watch [BRUH Z-Wave Video](https://www.youtube.com/watch?v=ajklDCaOGwY) to learn before attempting setup.
   - [Fibaro Gen 5 Multisensor (FGMS-001-ZW5-UK)](http://amzn.to/2wrJK0g)
     - Home Assistant Component: [z-wave](https://home-assistant.io/components/zwave/) plus sub components
     - Provides: A range of movement, light and temperature sensors in a single battery powered device.
     - Limitations:
       - Setup may take multiple attempts. Watch [BRUH Z-Wave Video](https://www.youtube.com/watch?v=ajklDCaOGwY) to learn before attempting setup.
       - No humidty sensor
       - Battery only, which means it goes to sleep a lot to save power. Currently testing in parallel to see if that really matters.
 - A range of other 433Mhz devices:
   - Home Assistant Component: [RfxTrx](https://home-assistant.io/components/rfxtrx/)
   - Device: Owl Energy Monitor
     - Notes: Still being investigated
   - Device: Internal Temperature and Humidity monitors [WH5](http://www.ebay.co.uk/itm/Extra-Sensor-for-Weather-Station-with-temp-humidity-f-cast-base-Baro-press/261788376051)
     - Notes: Temperature readings from WH5 are 40 DegC higher than they should be. This can be corrected by use of a template i.e. `value_template: '{{ (states.sensor.temp_humid_1_temperature.attributes["Temperature"] | float - 40) | round(1) }}'`
     - Research page: [Glen Pitt-Pladdy Blog](https://www.pitt-pladdy.com/blog/_20131228-233456_0000_Imagintronix_Temperature_Humidity_Sensor_Protocol_WH15B_for_WH1400_/)
   - Device: External Temperature and Humidty sensor, Oregon THGN132N
     - Notes: Seems to work well, no special template required.
 - HP ILO sensor information
   - Home Assistant Component: [HP_ilo](https://home-assistant.io/components/sensor.hp_ilo/)
   - Provides: Sensor information for HP Servers with ILO such as overall health, temperature at specific points in the chassis.

### Software sensors
 - [Sun](https://home-assistant.io/components/sun/) - Provides details on sun posistion, enabling automation to be triggered, e.g. at dusk and dawn.
 - [Moon](https://home-assistant.io/components/sensor.moon/) - Provides details on the phase of the moon.
 - [System Monitor](https://home-assistant.io/components/sensor.systemmonitor/) - Provides information on the host system Home Assistant is running on.
 - [Home Assisatnt SSL Certificate Expiry Checking](https://home-assistant.io/docs/ecosystem/certificates/lets_encrypt/#7---set-up-a-sensor-to-monitor-the-expiry-date-of-the-certificate) - Provides a sensor to show the number of days until the current certificate in use expires. So that it can be renewed before it expirs.

### Location Tracking
 - iOS App - [Home Assistant App](https://itunes.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401)
   - Home Assistant 3rd Party Addon: [ios](https://home-assistant.io/docs/ecosystem/ios/)
   - Note: Also provides complete control of HASS, iPhone battery monitoring and is able to receive notifications from HASS.

# Other features being experimented with:
 - MQTT (configured not in use)
 - TTS (Text To Speech) via Google_SAY (configured not in use)
 
# Automation Scripts
- Turning on lights an hour before sunset
- Turning off power sockets if no movement detected for 30 mins and sockets drawing more than just standby power levels. Triggers notification when sockets are turned off.
- Send notification when Let's Encrypt SSL certificate used for HomeAssistant has less than 3 weeks left before expiry.

# Additional Info
Private information is stored in secrets.yaml (not uploaded)

# Config updating and validation
 - Changes to configuration are pushed to git using `gitupdate.sh` script.
 - TravisCI is connected to this repository, which will run a script validation for each check-in automatically. Setup as per: https://home-assistant.io/docs/ecosystem/backup/backup_github/
   - Note in order for Travis to work a number of extra files are required:
     - `travis_secrets.yaml` - Contains dummy values for the secrets used in the configuration files
     - `travis.fake_ssl_key` and `travis.fake_ssl_crt` - Are dummy files needed for a Home Assistant configuration setup to use SSL.