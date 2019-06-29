# Automation Scripts

## Utilities

- Automatically sync latest configuration from GitHub on a successful script validation via TravisCI. [Learn more](build_deploy.md)
- Send a notification when a new version of Home Assistant is made available.

## Backup

- HassIO provides a service which snapshots the configuration. 
- In combination with an [DropBox Sync add-on](https://github.com/danielwelch/hassio-dropbox-sync) and some automation scripts, it's possible to schedule regular snapshots and automatically upload these to DropBox.
- Automation is configured to perform a weekly snapshot, whilst checking for new snapshots to sync daily.

## Presence/Occupancy

- Control the heating, lights and cameras, depending on who is at home. 
- Send notifications when ooors or windows aren't closed.

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

## Have I Been Pwned Alerts

- Track all my email addresses and those of close family members. Triggering an alert notification to be sent when the number of breeches increases.
  - This requires the automation script be updated with a new value each time it increases. (I need to look at how/where I can persist this value)