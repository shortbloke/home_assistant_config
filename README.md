# Shortbloke's Home Assistant Configuration Files
[Home Assistant](https://home-assistant.io) Configuration Files [![Build Status](https://travis-ci.org/shortbloke/home_assistant_config.svg?branch=master)](https://travis-ci.org/shortbloke/home_assistant_config)

This is my currently active set of configuration files for my HomeAssistant running on Raspberry Pi. Integrating with:

 ## Devices:
 - Amazon Echo / Alexa
   - Uses: Emulated Hue component for quicker interactions between Echo and devices.
 - HP ILO sensor information
 - LightwaveRF (via (RFXtrx) Devices:
   - Plug in sockets (JSJSLW321)
   - Inline Dimmer module (JSJSLW831)
   - Smartphone Web Link - Hub (JSJSLW930)
 - Belkin Wemo Insight switch
 - TP-Link HS110 Smart Plug with energy monitoring
 - Nest Thermostat (3rd generation) and Nest Protect (2nd generation)
 - Plex Media Server
 - Sonos
 - Z-Wave Devices:
   - Aeotec Z-Stick Gen 5 (ZW090)
   - Aeotec Multisensor 6 (ZW100)
   - Fibaro Gen 5 Multisensor (FGMS-001-ZW5-UK)
 - A range of other 433Mhz devices are also monitored and controlled via RFXtrx including:
   - Flamerite Eletric Fire
   - Owl Energy Monitor
   - Temperature + Humidity sensors (External: Oregon THGN132N, Internal: [WH5](https://www.pitt-pladdy.com/blog/_20131228-233456_0000_Imagintronix_Temperature_Humidity_Sensor_Protocol_WH15B_for_WH1400_/))
     - Note: WH5 reports temp +20 degC, so this needs to be subtracted.
   - various other 433Mhz switches I've detected and now ignore as they aren't in my house

## Location Tracking:
- via iOS App - [Home Assistant App](https://itunes.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401)
  - Also provides complete control of HASS, iPhone battery monitoring and is able to receive notifications from HASS.

## Other features being experimented with:
 - MQTT (configured not in use)
 - TTS (Text To Speech) via Google_SAY (configured not in use)
 
## Automation Scripts:
- Turning on lights an hour before sunset
- Turning off power sockets if no movement detected for 30 mins and sockets drawing more than just standby power levels. Triggers notification when sockets are turned off.
- Send notification when Let's Encrypt SSL certificate used for HomeAssistant has less than 3 weeks left before expiry.

## Additional Info:
Private information is stored in secrets.yaml (not uploaded)

## Useful links:
A couple of useful reference for getting up config file tracking in git:
- [Arsaboo CheatSheet](https://github.com/arsaboo/homeassistant-config/blob/master/HASS%20Cheatsheet.md)
- [Home Assistant Cookbook example](https://home-assistant.io/cookbook/githubbackup/)
