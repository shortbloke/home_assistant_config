 
# Automation Scripts
## Utilities
 * Automatically sync latest configuration from github on a successful script validation via TravisCI. [Learn more](build_deploy.md)

## Power Control
 * Turning on specific lights 1 hour before sunset
 * Turn on a Sonoff relay switch when loft temperatures get high and off again when they lower
   * This is used to power an inline fan which pulls cooler air from outside to the front of my HP Microserver
 * If there is no movement in a room turn off any TP Link Smart socket which is drawing power and send an alert
   * Aim to ensure various appliances aren't left on accidentally
   * This ensures smart switches aren't turned off just because they are on, only when something connected to them is drawing power

## Power Control of Mining Rigs
 * Monitoring power consumption of TP Link HS110 sockets with mining rigs connected. To act as final watchdog reset should mining software not recover the system or the system is locked up.
   * Send a notification if power consuption lower than threshold for 20mins.
   * Power off socket, wait 1 min then power on again, if power consumption lower than threshold for 30mins. 

 ## Home Assistant Resource Usage Alerts
  * Monitor system resources and send alters to specific IOS device when thresholds breached. Items monitored:
    * High Load Average
    * Low Disk Space
    * Low Memory