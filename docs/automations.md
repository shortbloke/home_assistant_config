# Automations and Scripts

## Backup

- Backups are managed by the [Home Assistant Google Drive Backup add-on](https://github.com/sabeechen/hassio-google-drive-backup).

## Presence/Occupancy

- Control the heating and lights, depending on who is at home.
- Send notifications when doors or windows aren't closed.

## Heating Control

- When the back door is left open for one minute, store the thermostat temperature and reduce it to 15°C. Restore the stored temperature when the door closes.
- Every hour at 15 minutes past, turn on the conservatory heater when the temperature is below 18°C, the back door is closed and the time is between 06:00 and 23:00.
- Turn off the conservatory heater when the temperature rises above 21°C. During the night, turn it off at 23:00 or when the temperature rises above 18°C.

## Power Control

- Turn on selected lights in the morning and one hour before sunset.
- Turn on a Tasmota relay when the loft temperature rises above 30°C and turn it off when the temperature drops below 30°C. The relay powers an inline fan that draws cooler air towards the server.
- Turn the 3D-printer light on and off based on the printer's power consumption.
- Enforce a television curfew and optionally announce a reminder over Sonos.

## Iron Safety

- Track occupancy in the ironing room and change its state to idle after 30 minutes without motion.
- If an iron is drawing more than 10 W while the room is idle, notify the user and turn off its smart plug.

## Kitchen Appliance Monitoring

- Track washing-machine, tumble-dryer and dishwasher power usage to determine when a cycle starts and finishes, then send a completion notification.

## Safety and Monitoring

- Notify when a monitored Zigbee device, iron smart plug or gas-meter sensor is unavailable.
- Notify mobile devices and announce over the kitchen Sonos speaker when water is detected under the kitchen sink.
- Provide a burglar-alarm script that sounds configured Sonos speakers and Ring sirens for 30 seconds.
- Alert when the Owl electricity feed has stopped updating for an hour and notify again when reporting recovers.
- Alert when the water-softener salt level is low.

## Energy and Electric Vehicle Charging

- Detect when Tesla charging starts and finishes.
- Dynamically adjust Tesla charging current to use available solar generation while allowing a small grid-import tolerance.

## Home Assistant Resource Usage Alerts

- Monitor system resources and send alerts to a specific iOS device when thresholds are breached. Items monitored:
  - High Load Average
  - Low Disk Space
  - Low Memory
