# Automation Scripts

## Utilities

- Automatically sync latest configuration from GitHub on a successful script validation via TravisCI. [Learn more](build_deploy.md)
- Send a notification when a new version of Home Assistant is made available.

## Backup

- HassIO provides a service which snapshots the configuration. Originally I set this up with dropbox sync and some automation scripts. I've since switched to the [Home Assistant Google Drive Backup add-on](https://github.com/sabeechen/hassio-google-drive-backup) which is a simpler solution.

## Presence/Occupancy

- Control the heating and lights, depending on who is at home.
- Send notifications when doors or windows aren't closed.

## Heating Control

- When the back door (ZigBee sensor) is left open, then Nest Heating Operation Mode is set to Eco. Once the door is closed it's returned to it's previous state (off, heat or eco)

## Power Control

- Turning on specific lights in the morning and 1 hour before sunset
- Turn on a Sonoff relay switch when loft temperatures get high and off again when they lower
  - This is used to power an inline fan which pulls cooler air from outside to the front of my HP MicroServer
  - If there is no movement in a room turn off any TP Link Smart socket which is drawing power and send an alert
  - Aim to ensure various appliances aren't left on accidentally
  - This ensures smart switches aren't turned off just because they are on, only when something connected to them is drawing power

## Kitchen Appliance Monitoring

- Track power usage of kitchen appliances to determine when they have been turned on, and when they complete their cycle. Sending a notification when they finish.

## Plant monitoring

- Send notification when plants soil falls below specified minimum for each plant type.

## Home Assistant Resource Usage Alerts

- Monitor system resources and send alters to specific IOS device when thresholds breached. Items monitored:
  - High Load Average
  - Low Disk Space
  - Low Memory
