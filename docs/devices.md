# Devices Controlled by Home Assistant

The following devices are controlled via my Home Assistant configurations. They may also provide sensors as input.

## Appliances

| Device | Functionality |
| ---| --- |
| [LG FH4G1BCS2](https://amzn.to/3HjoCj4) Washing Machine| Component: [ha-smartthinq-sensors](https://github.com/ollo69/ha-smartthinq-sensors) via HACS<br>Device provides details of active washing program<br><br>Limitations:<ul><li>No official support, requires using HACS.</li><li>Requires an an LG account. Note federated/social accounts can't be used.</li><li>Power monitoring data not provided.</li></ul> |
| [LG FDV909WN](https://amzn.to/49DcbtT) Tumble Dryer| Component: [ha-smartthinq-sensors](https://github.com/ollo69/ha-smartthinq-sensors) via HACS<br>Device provides details of active drying program<br><br>Limitations:<ul><li>No official support, requires using HACS.</li><li>Requires an an LG account. Note federated/social accounts can't be used.</li><li>Power monitoring data not provided.</li></ul> |
| [Flamerite](http://www.flameritefires.com/products/floor-standing-suites/junai.html) Electric Fire| Component: [switch.rfxtrx](https://home-assistant.io/components/switch.rfxtrx/)<br>Our flamerite fire came with a 433Mhz remote control. The RFXCOM 433 Transceiver was able to detect the codes from the remote and allow Home Assistant to send the same codes|

## Climate Control

| Device | Functionality |
| ---| --- |
| [Nest Thermostat (3rd generation)](http://amzn.to/2umTkEp) | Component: via HomeBridge and HomeBridge Nest Plugin<br>Temperature, heating, hot water and protect control and monitoring<br><br>Limitations:<ul><li>Uses community add-on to enable HomeBridge to be installed see [add-on instructions](https://github.com/davide125/hassio-addons/tree/main/homebridge).</li></ul> |
| [CHOSRY WiFi Fused Spur](https://amzn.to/3wcDsp2) | Component: [HACS Custom Component: hass-localtuya](https://github.com/xZetsubou/hass-localtuya)<br>WiFi controlled 13A fused spur with energy monitoring, connected to panel heater in conservatory. Allowing automations to drive when the the heater is active, rather than relying on the onboard timer and thermostat. |

## Security

| Device | Functionality |
| ---| --- |
| [Ring Floodlight Cam](https://en-uk.ring.com/products/floodlight-cam) | Component: [Ring](https://www.home-assistant.io/components/ring/)<br>Floodlight with motion activated camera.<br><br>Limitations:<ul><li>No live view of video via HomeAssistant</li><li>Unable to trigger the camera to start recording</li></ul> |

## Gas, Electricity and Solar Generation Monitoring

| Device |  Functionality |
| ---| --- |
| Modified Zigbee magnetic Sensor [Xiaomi Aqara Window or Door Magnetic Sensor](https://amzn.to/3rETLFD)| Component: [ZigBee Home Automation](https://www.home-assistant.io/components/zha/)<br>Removing the reed switch from the existing sensor and connecting an [external reed switch](https://amzn.to/37w5wqX) which senses the dial on the gas meter rotating, enables accurate measurement of gas usage which can be added to the Energy Dashboard. |
| [Owl Intuition PV](https://amzn.to/2Ufm6Q6) | Addon: [Node Red](https://github.com/hassio-addons/addon-node-red)<br>Component: [Custom Component : node-red-contrib-home-assistant-websocket](https://github.com/zachowj/node-red-contrib-home-assistant-websocket)<br>Component: [Custom Component : Node-RED Companion Integration](https://github.com/zachowj/hass-node-red)<br><br>I was using [Custom Component : Owl Intuition](https://github.com/custom-components/sensor.owlintuition) however, this was appears to have got slower over time and doesn't always send updates. So I've swiched to using a Node-RED flow [owl_node_red_flow.json](owl_node_red_flow.json). This provides frequent updates based on decoding to the UDP packets sent to the UDP listener. It updates sensors in Home Assistant using the HACS component [Node-RED Companion Integration](https://github.com/zachowj/hass-node-red) Captures electricity usage from multiple current sensors attached to power cable near the electricity meter, in order to detect total power usage, electricity being generated and also what is being exported back to the grid.<br><br>Limitations:<ul><li>Requires active Owl Intuition Subscription in order to use the Owl Web Portal to configure the IP address on the LAN to send packets to, e.g. The HomeAssistant machine. It is also required to enter the cost per unit of electricity which is then sent back down to the Network Owl</li><li>The Network OWL supports a UDP broadcast of the data, which would negate the need for the Owl Subscription, once you have it all setup.</li></ul> |

## Power and Lighting control

| Device |  Functionality |
| ---| --- |
| [Lightwave RF Devices](https://www.lightwaverf.com) <ul><li>Plug in sockets ([JSJSLW321](http://amzn.to/2vN1oys))</li><li>Inline Dimmer module ([JSJSLW831](http://amzn.to/2vLdcjH))</li><li>Smartphone Web Link - Hub ([JSJSLW930](http://amzn.to/2vLbJKq)) (Note: Not needed for Home Assistant Control)</li></ul> | Component: [RFXtrx](https://home-assistant.io/components/rfxtrx/)<br>LightwaveRF devices provide an easy solution for retrofitting automation into existing homes. Many other technologies require both Live and Neutral to be present at light switches, which is uncommon for UK installations at least<br><br>Limitations:<ul><li>One-Way communication, you can not query state to know devices status, nor can you confirm if commands sent were obeyed.</li></ul> |
| Zigbee RGB Controller <ul><li>[RGBW Controller](https://s.click.aliexpress.com/e/_AStgXx)</li></ul> | Component: [ZigBee Home Automation](https://www.home-assistant.io/components/zha/)<br>Zigbee 3.0 connected RGBW Lighting controller. Used in conjunction with RGBW light strips. See my installation [Multi-zone WiFi LED Lighting](https://www.martinrowan.co.uk/2018/02/multi-zone-wifi-led-lighting-part-3-installation/), though this was initially done using WiFi controllers, I've since switched to Zigbee as I had issues with the WiFi controllers frequently disconnecting from the network.</ul> |
| [TP-Link HS110, KP115 & Tapo P110](https://amzn.to/3ws5kVG) WiFi Smart Plug with energy monitoring| Component: [TP-Link Smart Home](https://www.home-assistant.io/integrations/tplink/) <br>WiFi controlled plugin adapter with Energy monitoring. Enabling actions/automation to be triggered based on power usage. |
| [Sonoff WiFi Relay Modules](http://sonoff.itead.cc/en/) (with modified hardware and firmware) <ul><li>Inline 10A Relay ([Sonoff Switch](http://amzn.to/2xmjjIY))</li><li>Inline 16A Relay with temperature and humidity monitoring ([Sonoff TH16](http://amzn.to/2wiJKm0))</li></ul> | Component: [MQTT Switch](https://home-assistant.io/components/switch.mqtt/)<br>Simple MQTT enabled wifi relay/switches and sensors at an incredibly low cost. With modifications: <ul><li>Hardware modified by soldering headers onto Sonoff board to enable custom firmware updating.</li><li>Custom Firmware to provide simple web configuration and control and MQTT support. Currently using [Sonoff-Tasmota](https://github.com/arendst/Sonoff-Tasmota) additional information  in the [project wiki](https://github.com/arendst/Sonoff-Tasmota/wiki)</li></ul>Limitations:<ul><li>Need to open up devices and solder headers to flash custom firmware.</li><li>Need to flash custom firmware via [3.3V FTDI USB-to-Serial Converter/Programmer](http://amzn.to/2xlYJIw) (Be sure to set USB to serial programmer to **3.3V**, it may be 5V by default (mine was) and will likely kill the ESP8266 is you supply it with 5V.)</li><li>Need to setup MQTT Broker on Raspberry Pi. I'm using Mosquitto. [Useful setup video](https://www.youtube.com/watch?v=AsDHEDbyLfg)</li><li>The TH16 Device is CE marked and having compared the design to the original switch, with a fuse and greater separation between High and Low voltage components.</li><li>The Sonoff Basic switch is not CE certified, based on the [CE Certification](https://www.itead.cc/wiki/File:CE_Certificate_for_Sonoff_Series.pdf) document. Caution should be used with this device.</li></ul> |

## Media Players

| Device | Functionality |
| ---| --- |
| [Sonos](http://www.sonos.com) | Component: [mediaplayer.sonos](https://home-assistant.io/components/media_player.sonos/)<br>Automatic detection of all Sonos Devices. Shows what is playing on each device. Able to control playback. Also able to be integrated with Text to Speech components |
| [Plex](http://www.plex.tv) | Component: [mediaplayer.plex](https://home-assistant.io/components/media_player.plex/)<br>Shows activity of Plex Clients |
| [Samsung Smart TVs](http://www.samsung.com/uk/tvs/all-tvs/) | Component: [mediaplayer.samsungtv](https://home-assistant.io/components/media_player.samsungtv/)<br>Discovery component will automatically detect TVs, report status and can be controlled via component<br><br>Limitations:<ul><li>Not all Smart TV models are fully supported.</li></ul> |

## Voice Control

| Device |  Functionality |
| ---| --- |
| [Amazon Echo Dot (2nd Generation)](http://amzn.to/2unxhgz) | Component: [Alexa](https://www.home-assistant.io/integrations/alexa/)<br>Voice control input to Home Assistant. Uses an AWS lambda to provide route information to Alexa from HomeAssistant |

## Hardware Sensors

| Device | Functionality |
| ---| --- |
| ZigBee: [Xiaomi Aqara TH1](https://amzn.to/44gEUmT) Temperature Humidity Sensor | Component: [ZigBee Home Automation](https://www.home-assistant.io/components/zha/)<br>A compact wireless battery powered temperature and humidity sensor.<br><br>Limitations:<ul><li>None yet.</li></ul> |
| Zigbee: [Sonff SNZB-02P](https://amzn.to/3Wem6Te) Temperature & Humidty Sensor | Component: [ZigBee Home Automation](https://www.home-assistant.io/components/zha/)<br>A battery powered temperature and humidty sensor with claimed 4 year battery life due to larger CR2477 battery.<br><br>Limitations:<ul><li>None yet.</li></ul> |
| ZigBee: [Xiaomi Aqara Window or Door Magnetic Sensor ](https://amzn.to/3UiYM43) | Component: [ZigBee Home Automation](https://www.home-assistant.io/components/zha/)<br>A compact battery powered magnetic sensor for use on doors and windows.<br><br>Limitations:<ul><li>None yet.</li></ul> |
| BLE: [Xiaomi Mi Flora Plant Sensor](https://amzn.to/3y3vM8U) | Component: [Mi Flora plant sensor](https://www.home-assistant.io/components/miflora/)<br>A compact battery powered plant sensor.<br><br>Limitations:<ul><li>Bluetooth Low Energy range is limited.</li><li>ZigBee Shield required Bluetooth be disabled, so on board Bluetooth wasn't available.</li></ul>Workaround:<ul><li>Component: [Plant](https://www.home-assistant.io/components/plant/)</li><li>BLE->MQTT: [Xiaomi Mi Flora Plant Sensor MQTT Client/Daemon](https://github.com/ThomDietrich/miflora-mqtt-daemon)</li><li>Hosted on: [Raspberry Pi Zero W](https://amzn.to/2ZLhm7d)</li></ul>|


## Software Sensors

| Component | Functionality |
| --- | --- |
| iOS App [Home Assistant App](https://itunes.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401) | With Home Assistant addon [ios](https://home-assistant.io/docs/ecosystem/ios/) enables location tracking plus complete control of HASS, iPhone battery monitoring and is able to receive notifications from Home Assistant |
| [Sun](https://home-assistant.io/components/sun/) | Sun position, enabling automation to be triggered, e.g. at dusk and dawn |
| [System Monitor](https://home-assistant.io/components/sensor.systemmonitor/) | System resource usage information on the host system Home Assistant is running on |
