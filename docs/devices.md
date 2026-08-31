# Devices Controlled by Home Assistant

The following devices are controlled or monitored by Home Assistant.

## Home Assistant Hub

| Device | Functionality |
| --- | --- |
| Raspberry Pi 5 with Argon ONE V5 | Runs Home Assistant OS directly from a 250 GB NVMe drive. The enclosure provides passive cooling, temperature-controlled fan cooling and an OLED status display. See [Migrating Home Assistant to an Argon ONE V5](https://www.martinrowan.co.uk/2026/08/migrating-home-assistant-to-argon-one-v5/). |
| [Argon Industria Zigbee Module](https://argon40.com/en-gb/products/argon-industria-v5-zigbee-module) | Integration: [Zigbee Home Automation](https://www.home-assistant.io/integrations/zha/).<br>Internal Texas Instruments CC2652 Zigbee coordinator. The Zigbee network was migrated from the previous Nortek USB coordinator without re-pairing the devices. |
| RFXCOM RFXtrx433E | Integration: [RFXtrx](https://www.home-assistant.io/integrations/rfxtrx/).<br>External USB radio for receiving and transmitting supported 433 MHz protocols. |

## Appliances

| Device | Functionality |
| --- | --- |
| [LG FH4G1BCS2](https://amzn.to/3HjoCj4) washing machine | Integration: [ha-smartthinq-sensors](https://github.com/ollo69/ha-smartthinq-sensors) via HACS.<br>Provides details of the active washing programme.<br><br>Limitations:<ul><li>No official support; requires HACS.</li><li>Requires an LG account. Federated or social accounts cannot be used.</li><li>Power-monitoring data is not provided.</li></ul> |
| [LG FDV909WN](https://amzn.to/49DcbtT) tumble dryer | Integration: [ha-smartthinq-sensors](https://github.com/ollo69/ha-smartthinq-sensors) via HACS.<br>Provides details of the active drying programme.<br><br>Limitations:<ul><li>No official support; requires HACS.</li><li>Requires an LG account. Federated or social accounts cannot be used.</li><li>Power-monitoring data is not provided.</li></ul> |
| [Flamerite](http://www.flameritefires.com/products/floor-standing-suites/junai.html) electric fire | Integration: [RFXtrx](https://www.home-assistant.io/integrations/rfxtrx/).<br>The fire uses a 433 MHz remote control. The RFXCOM transceiver receives its codes and allows Home Assistant to transmit the same commands. |

## Climate Control

| Device | Functionality |
| --- | --- |
| [Nest Thermostat (3rd generation)](http://amzn.to/2umTkEp) | Integrated through Homebridge using the [Nest Accfactory plugin](https://github.com/n0rt0nthec4t/homebridge-nest-accfactory) and HomeKit Device.<br>Provides temperature, heating and hot-water control and monitoring.<br><br>Limitations:<ul><li>Requires Homebridge and the Nest Accfactory plugin.</li></ul> |
| [CHOSRY Wi-Fi Fused Spur](https://amzn.to/3wcDsp2) | Integration: [LocalTuya](https://github.com/xZetsubou/hass-localtuya) via HACS.<br>Wi-Fi-controlled 13 A fused spur with energy monitoring, connected to the conservatory panel heater. Automations control when the heater is active instead of relying on its onboard timer and thermostat. |

## Security

| Device | Functionality |
| --- | --- |
| [Ring Floodlight Cam Pro (4K)](https://amzn.to/48pXN9l)<br><br>[Ring Wired Doorbell Pro](https://amzn.to/48Hjdjq)<br><br>[Ring Indoor Camera](https://amzn.to/48tK8yd)<br><br>[Ring Pan-Tilt Indoor Camera](https://amzn.to/4pJPo7T)<br><br>[Ring Outdoor Camera Plus](https://amzn.to/4p7oMNV) | Integration: [ring-mqtt](https://github.com/tsightler/ring-mqtt).<br><br>Limitations:<ul><li>Only camera snapshots are available in Home Assistant, not live video.</li><li>ring-mqtt must be added to the add-on store.</li></ul> |

## Gas, Electricity and Solar Generation Monitoring

| Device | Functionality |
| --- | --- |
| Modified [Xiaomi Aqara Window or Door Sensor](https://amzn.to/3rETLFD) | Integration: [Zigbee Home Automation](https://www.home-assistant.io/integrations/zha/).<br>The original reed switch was replaced with an [external reed switch](https://amzn.to/37w5wqX) that detects rotation of the gas-meter dial. This provides gas-usage measurements for the Energy dashboard. |
| [Owl Intuition PV](https://amzn.to/2Ufm6Q6) | Add-on: [Node-RED](https://github.com/hassio-addons/addon-node-red).<br>Integrations: [Node-RED Companion](https://github.com/zachowj/hass-node-red) and [node-red-contrib-home-assistant-websocket](https://github.com/zachowj/node-red-contrib-home-assistant-websocket).<br><br>The previous Owl Intuition custom integration became slow and unreliable, so it was replaced by the [Node-RED flow](owl_node_red_flow.json). The flow decodes UDP packets and publishes electricity usage, solar generation and grid-export sensors to Home Assistant.<br><br>Limitations:<ul><li>An active Owl Intuition subscription is required to use the Owl portal to configure the Home Assistant host as the LAN destination and send tariff settings to the Network OWL.</li><li>Once configured, the Network OWL can broadcast the data over UDP without the subscription.</li></ul> |

## Power and Lighting Control

| Device | Functionality |
| --- | --- |
| [Lightwave RF devices](https://www.lightwaverf.com/) | Integration: [RFXtrx](https://www.home-assistant.io/integrations/rfxtrx/).<br>Provides control of plug-in sockets and inline dimmer modules through the RFXCOM transceiver.<br><br>Limitations:<ul><li>Communication is one-way, so Home Assistant cannot query state or confirm that commands were received.</li></ul> |
| Zigbee RGBW controllers | Integration: [Zigbee Home Automation](https://www.home-assistant.io/integrations/zha/).<br>Controls RGBW light strips. These replaced earlier Wi-Fi controllers that disconnected frequently. |
| [Sonoff Zigbee smart plugs](https://link.amazon/B04dnxy4x) | Integration: [Zigbee Home Automation](https://www.home-assistant.io/integrations/zha/).<br>Provides remote power control through the Zigbee network. |
| [TP-Link HS110, KP115 and Tapo P110](https://amzn.to/3ws5kVG) smart plugs | Integration: [TP-Link Smart Home](https://www.home-assistant.io/integrations/tplink/).<br>Wi-Fi-controlled smart plugs with energy monitoring, used by appliance-monitoring and safety automations. |
| Sonoff relay modules | Integration: [Tasmota](https://www.home-assistant.io/integrations/tasmota/) over MQTT.<br>The devices run Tasmota firmware and provide relay, temperature and humidity data where supported.<br><br>Limitations:<ul><li>Installing custom firmware requires opening the device, soldering headers and using a 3.3 V serial adapter.</li><li>The MQTT broker and MQTT integration must be available.</li></ul> |

## Media Players and Text-to-Speech

| Device | Functionality |
| --- | --- |
| [Sonos](https://www.sonos.com/) | Integration: [Sonos](https://www.home-assistant.io/integrations/sonos/).<br>Discovers Sonos speakers, reports playback state and provides playback controls. The `sonos_say` script uses the modern `tts.speak` action with the Google Translate UK English TTS entity. It snapshots playback, makes an announcement and restores the previous state. |
| [Plex](https://www.plex.tv/) | Integration: [Plex Media Server](https://www.home-assistant.io/integrations/plex/).<br>Shows activity from Plex clients. |
| [Samsung Smart TVs](https://www.samsung.com/uk/tvs/all-tvs/) | Integration: [Samsung Smart TV](https://www.home-assistant.io/integrations/samsungtv/).<br>Discovers supported televisions, reports their state and provides controls.<br><br>Limitations:<ul><li>Not all television models are fully supported.</li></ul> |

## Voice Control

| Device | Functionality |
| --- | --- |
| [Amazon Echo Dot (2nd generation)](http://amzn.to/2unxhgz) | Integration: [Alexa Smart Home](https://www.home-assistant.io/integrations/alexa/).<br>Provides voice control through an AWS Lambda function that routes Alexa requests to Home Assistant. |

## Hardware Sensors

| Device | Functionality |
| --- | --- |
| Zigbee [Xiaomi Aqara TH1](https://amzn.to/44gEUmT) temperature and humidity sensor | Integration: [Zigbee Home Automation](https://www.home-assistant.io/integrations/zha/).<br>A compact, wireless, battery-powered temperature and humidity sensor. |
| Zigbee [Sonoff SNZB-02P](https://amzn.to/3Wem6Te) temperature and humidity sensor | Integration: [Zigbee Home Automation](https://www.home-assistant.io/integrations/zha/).<br>A battery-powered sensor with a claimed four-year battery life from its larger CR2477 battery. |
| Zigbee [Xiaomi Aqara Window or Door Sensor](https://amzn.to/3UiYM43) | Integration: [Zigbee Home Automation](https://www.home-assistant.io/integrations/zha/).<br>A compact, battery-powered magnetic sensor for doors and windows. |

## Software Sensors

| Integration | Functionality |
| --- | --- |
| [Home Assistant Companion App for iOS](https://companion.home-assistant.io/) | Provides location tracking, Home Assistant controls, device sensors and push notifications. |
| [Sun](https://www.home-assistant.io/integrations/sun/) | Provides the Sun's position for automations such as lighting at dawn and dusk. |
| [System Monitor](https://www.home-assistant.io/integrations/systemmonitor/) | Provides resource-usage information for the Home Assistant host. |
