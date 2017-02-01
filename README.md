# Shortbloke's Home Assistant Configuration Files
[Home Assistant](https://home-assistant.io) Configuration Files 

This is my currently active set of configuration files for my HomeAssistant running on Raspberry Pi. Integrating with:

 - Amazon Echo / Alexa
 - Emulated Hue (quicker integration between Echo and LightwaveRF)
 - HP ILO sensor information
 - iCloud device tracking (*REMOVED DUE TO HIGH BATTERY DRAIN*)
 - IFTTT
 - LightwaveRF (via RFXtrx) - Lights, Switched sockets and more to follow
 - MQTT
 - Nest
 - Plex
 - RFXtrx (RFXtrx433)
 - Sonos
 - TTS (Text To Speech) via Google_SAY
 - Wemo
 - Other 433Mhz devices are also monitored and controlled including:
   - Flamerite Eletric Fire
   - Owl Energy Monitor
   - Temperature + Humidity sensors (External: Oregon THGN132N, Internal: [WH5](https://www.pitt-pladdy.com/blog/_20131228-233456_0000_Imagintronix_Temperature_Humidity_Sensor_Protocol_WH15B_for_WH1400_/)
     - Note: WH5 reports temp +20 degC, so this needs to be subtracted.
   - various other 433Mhz switches I've detected and now ignore as they aren't in my house

Private information is stored in secrets.yaml (not uploaded)

A couple of useful reference for getting up config file tracking in git:
- [Arsaboo CheatSheet](https://github.com/arsaboo/homeassistant-config/blob/master/HASS%20Cheatsheet.md)
- [Home Assistant Cookbook example](https://home-assistant.io/cookbook/githubbackup/)
