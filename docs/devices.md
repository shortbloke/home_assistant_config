# Devices Controlled by Home Assistant

The following devices are controlled via my Home Assistant configurations. They may also provide sensors as input.

## Climate Control

| Device | Functionality |
| ---| --- |
| [Nest Thermostat (3rd generation)](http://amzn.to/2umTkEp) | Component: [Nest](https://home-assistant.io/components/nest/)<br>Temperature sensors and heating status information along with target temperature being able to be controlled via Home Assistant<br><br>Limitations:<ul><li>Requires setup of a Nest Developer account (free)</li><li>Whilst 3rd gen Nest Thermostat in the UK provides the ability to control the hot water system. This isn't exposed via current implementation in Home Assistant.</li></ul> |

## Security

| Device | Functionality |
| ---| --- |
| [Ring Floodlight Cam](https://en-uk.ring.com/products/floodlight-cam) | Component: [Ring](https://www.home-assistant.io/components/ring/)<br>Floodlight with motion activated camera.<br><br>Limitations:<ul><li>No live view of video via HomeAssistant</li><li>Unable to trigger the camera to start recording</li></ul> |

## Electricity and Solar Generation Monitoring

| Device |  Functionality |
| ---| --- |
| [Owl Intuition PV](https://amzn.to/2Ufm6Q6) | Component: [Custom Component : Owl Intuition](https://github.com/custom-components/sensor.owlintuition)<br>Captures electricity usage from multiple current sensors attached to power cable near the electricity meter, in order to detect total power usage, electricity being generated and also what is being exported back to the grid.<br><br>Limitations:<ul><li>Requires active Owl Intuition Subscription in order to use the Owl Web Portal to configure the IP address on the LAN to send packets to, e.g. The HomeAssistant machine. It is also required to enter the cost per unit of electricity which is then sent back down to the Network Owl</li><li>The Network OWL supports a UDP broadcast of the data, which would negate the need for the Owl Subscription, however this doesn't appear to be supported.</li></ul> |

## Power and Lighting control

| Device |  Functionality |
| ---| --- |
| [Lightwave RF Devices](https://www.lightwaverf.com) <ul><li>Plug in sockets ([JSJSLW321](http://amzn.to/2vN1oys))</li><li>Inline Dimmer module ([JSJSLW831](http://amzn.to/2vLdcjH))</li><li>Smartphone Web Link - Hub ([JSJSLW930](http://amzn.to/2vLbJKq)) (Note: Not needed for Home Assistant Control)</li></ul> | Component: [RFXtrx](https://home-assistant.io/components/rfxtrx/)<br>LightwaveRF devices provide an easy solution for retrofitting automation into existing homes. Many other technologies require both Live and Neutral to be present at light switches, which is uncommon for UK installations at least<br><br>Limitations:<ul><li>One-Way communication, you can not query state to know devices status, nor can you confirm if commands sent were obeyed.</li></ul> |
| [Smart Life (Tuya)](https://www.tuya.com/) <ul><li>[RGB GU10 Lights](https://amzn.to/2RhODCH)</li></ul> | Component: [Tuya](https://www.home-assistant.io/components/tuya/)<br>WiFi (2.4Ghz) connected GU10 bulbs providing RGB and white light. IOS and Android app along with support for Alexa and Google Home.<br><br>Limitations:<ul><li>Needs to register an account via the mobile App to setup and control the lights.</li><li>Not locally controlled, requires outbound internet connection to 3rd party cloud service.</li><li>Each bulb requires it's own IP address, a large deployment might require changes to local network configuration.</li></ul> |
| Flux LED (MagicLight) <ul><li>[UFO RGBW Controller](https://amzn.to/2OcNY3h)</li></ul> | Component: [Flux_Led](https://www.home-assistant.io/components/light.flux_led/)<br>WiFi (2.4Ghz) connected RGBW Lighting controller. Used in conjunction with RGBW light strips. See my installation [Multi-zone WiFi LED Lighting](https://www.martinrowan.co.uk/2018/02/multi-zone-wifi-led-lighting-part-3-installation/). IOS and Android app along with support for Alexa and Google Home. App discovers devices on local network. Alexa and Google home control requires a skill and a cloud account.<br><br>Limitations:<ul>Sometimes the controllers drop off the wireless network and need to be power cycled. Doing so occasionally loses the current network configuration, so that the controlled needs to be re-initialised and joined to the local wireless network.</ul> |
| [TP-Link HS110 WiFi Smart Plug with energy monitoring](http://amzn.to/2vgQU8Q) | Component: [switch.tplink](https://home-assistant.io/components/switch.tplink/)<br>WiFi controlled plugin adapter with Energy monitoring. Enabling actions/automation to be triggered based on power usage. Similar to Belkin Wemo<br><br>Limitations:<ul><li>Nothing significant so far. I now have 3 of these devices to replace Wemo Insight Plugs. Hoping they last longer.</li></ul> |
| [Sonoff WiFi Relay Modules](http://sonoff.itead.cc/en/) (with modified hardware and firmware) <ul><li>Inline 10A Relay ([Sonoff Switch](http://amzn.to/2xmjjIY))</li><li>Inline 16A Relay with temperature and humidity monitoring ([Sonoff TH16](http://amzn.to/2wiJKm0))</li></ul> | Component: [MQTT Switch](https://home-assistant.io/components/switch.mqtt/)<br>Simple MQTT enabled wifi relay/switches and sensors at an incredibly low cost. With modifications: <ul><li>Hardware modified by soldering headers onto Sonoff board to enable custom firmware updating.</li><li>Custom Firmware to provide simple web configuration and control and MQTT support. Currently using [Sonoff-Tasmota](https://github.com/arendst/Sonoff-Tasmota) additional information  in the [project wiki](https://github.com/arendst/Sonoff-Tasmota/wiki)</li></ul>Limitations:<ul><li>Need to open up devices and solder headers to flash custom firmware.</li><li>Need to flash custom firmware via [3.3V FTDI USB-to-Serial Converter/Programmer](http://amzn.to/2xlYJIw) (Be sure to set USB to serial programmer to **3.3V**, it may be 5V by default (mine was) and will likely kill the ESP8266 is you supply it with 5V.)</li><li>Need to setup MQTT Broker on Raspberry Pi. I'm using Mosquitto. [Useful setup video](https://www.youtube.com/watch?v=AsDHEDbyLfg)</li><li>The TH16 Device is CE marked and having compared the design to the original switch, with a fuse and greater separation between High and Low voltage components.</li><li>The Sonoff Basic switch is not CE certified, based on the [CE Certification](https://www.itead.cc/wiki/File:CE_Certificate_for_Sonoff_Series.pdf) document. Caution should be used with this device.</li></ul> |
| [Flamerite Electric Fire](http://www.flameritefires.com/products/floor-standing-suites/junai.html) | Component: [switch.rfxtrx](https://home-assistant.io/components/switch.rfxtrx/)<br>Our famerite fire came with a 433Mhz remote control. The RFXCOM 433 Transceiver was able to detect the codes from the remote and allow Home Assistant to send the same codes |
| [Belkin Wemo Insight Switch, WiFi SmartPlug](http://amzn.to/2vMEtmN) | Component: [Wemo](https://home-assistant.io/components/wemo/)<br>WiFi controlled plugin adapter with Energy monitoring. Enabling actions/automation to be triggered based on power usage<br><br>Limitations:<ul><li>Questionable reliability: I've had two now fail with similar symptoms when turning off devices which pull a considerable current, ~18kW. This is significantly less than the 13A/240V rated maximum. I've now removed all Wemo Insight Plugs from my home. It's possible the current load readings from the Wemo were wrong, investigating.</li><li>Setup problems: Early firmware versions had problems with setup, especially in environments with multiple access points.</li><li>No memory of last power state. In the event of a recovery from a power cut, the device connected will remain off.</li></ul> |

## Media Players

| Device | Functionality |
| ---| --- |
| [Sonos](http://www.sonos.com) | Component: [mediaplayer.sonos](https://home-assistant.io/components/media_player.sonos/)<br>Automatic detection of all Sonos Devices. Shows what is playing on each device. Able to control playback. Also able to be integrated with Text to Speech components |
| [Plex](http://www.plex.tv) | Component: [mediaplayer.plex](https://home-assistant.io/components/media_player.plex/)<br>Shows activity of Plex Clients |
| [Samsung Smart TVs](http://www.samsung.com/uk/tvs/all-tvs/) | Component: [mediaplayer.samsungtv](https://home-assistant.io/components/media_player.samsungtv/)<br>Discovery component will automatically detect TVs, report status and can be controlled via component<br><br>Limitations:<ul><li>Not all Smart TV models are fully supported.</li></ul> |
| [Apple TV](https://www.apple.com/uk/tv/) | Component: [Apple_tv](https://home-assistant.io/components/apple_tv/)<br>(Only tested personally tested with Gen3 version) Shows what is playing on AppleTV with device controls. Plus provides access to a remote control. |

## Voice Control

| Device |  Functionality |
| ---| --- |
| [Amazon Echo Dot (2nd Generation)](http://amzn.to/2unxhgz) | Component: [Alexa](https://www.home-assistant.io/integrations/alexa/)<br>Voice control input to Home Assistant. Uses an AWS lambda to provide route information to Alexa from HomeAssistant |

## Hardware Sensors

| Device | Functionality |
| ---| --- |
| [Nest Protect (2nd generation) Smoke and Carbon monoxide detectors](http://amzn.to/2wFGOw4) | Component: [Nest](https://home-assistant.io/components/nest/)<br>Monitoring of Smoke and CO2 alarms and system health<br><br>Limitations:<ul><li>Requires setup of a Nest Developer account (free)</li></ul> |
| ZigBee: [Xiaomi Aqara Temperature Humidity Sensor ](https://www.ebay.co.uk/itm/Aqara-Smart-Temperature-Humidity-Sensor-ZigBee-Wifi-Wireless-Work-With-Xiaomi-UO/283185308376) | Component: [ZigBee Home Automation](https://www.home-assistant.io/components/zha/)<br>A compact wireless battery powered temperature and humidity sensor.<br><br>Limitations:<ul><li>None yet.</li></ul> |
| ZigBee: [Xiaomi Aqara Window or Door Magnetic Sensor ](https://www.ebay.co.uk/itm/Xiaomi-Aqara-ZigBee-Wireless-Smart-Window-Door-Sensor-Home-Security-App-Control/292555002431) | Component: [ZigBee Home Automation](https://www.home-assistant.io/components/zha/)<br>A compact battery powered magnetic sensor for use on doors and windows.<br><br>Limitations:<ul><li>None yet.</li></ul> |
| BLE: [Xiaomi Mi Flora Plant Sensor](https://www.ebay.co.uk/itm/Xiaomi-Mi-Battery-Bluetooth-APP-Flora-Monitor-Digital-Plant-Water-Care-Tester-UK/183834628232) | Component: [Mi Flora plant sensor](https://www.home-assistant.io/components/miflora/)<br>A compact battery powered plant sensor.<br><br>Limitations:<ul><li>Bluetooth Low Energy range is limited.</li><li>ZigBee Shield required Bluetooth be disabled, so on board Bluetooth wasn't available.</li></ul>Workaround:<ul><li>Component: [Plant](https://www.home-assistant.io/components/plant/)</li><li>BLE->MQTT: [Xiaomi Mi Flora Plant Sensor MQTT Client/Daemon](https://github.com/ThomDietrich/miflora-mqtt-daemon)</li><li>Hosted on: [Raspberry Pi Zero W](https://amzn.to/2ZLhm7d)</li></ul>|
| Other 433Mhz devices | Component: [RfxTrx](https://home-assistant.io/components/rfxtrx/)<ul><li>Owl Energy Monitor (investigating)</li><li>Internal Temperature and Humidity monitors [WH5](http://www.ebay.co.uk/itm/Extra-Sensor-for-Weather-Station-with-temp-humidity-f-cast-base-Baro-press/261788376051)</li><ul><li>Temperature readings from WH5 are 40 Deg C higher than they should be. This can be corrected by use of a template i.e. `value_template: "{{ (states.sensor.temp_humid_1_temperature.attributes['Temperature'] | float - 40) | round(1) }}"`</li><li>Research page: [Glen Pitt-Pladdy Blog](https://www.pitt-pladdy.com/blog/_20131228-233456_0000_Imagintronix_Temperature_Humidity_Sensor_Protocol_WH15B_for_WH1400_/)</li></ul><li>External Temperature and Humidity sensor, Oregon THGN132N |

## Software Sensors

| Component | Functionality |
| --- | --- |
| iOS App [Home Assistant App](https://itunes.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401) | With Home Assistant addon [ios](https://home-assistant.io/docs/ecosystem/ios/) enables location tracking plus complete control of HASS, iPhone battery monitoring and is able to receive notifications from Home Assistant |
| [Sun](https://home-assistant.io/components/sun/) | Sun position, enabling automation to be triggered, e.g. at dusk and dawn |
| [System Monitor](https://home-assistant.io/components/sensor.systemmonitor/) | System resource usage information on the host system Home Assistant is running on |
| [Travis-CI](https://home-assistant.io/components/sensor.travisci/) | Integrated test results from [Travis-CI](https://travis-ci.org/), providing the capability of automatically updating and restarting Home Assistant when files updated on github pass configuration checks in Travis CI. |
