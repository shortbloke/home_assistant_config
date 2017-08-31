 
# Automation Scripts
## Utilities
 * Trigger notification when SSL certificate used for Home Assistant site is expiry soon
 * Automatically sync latest configuration from github on a successful script validation via TravisCI. [Learn more](build_deploy.md)

## Power Control
 * Turning on specific lights 1 hour before sunset
 * Turn on a Sonoff relay switch when loft temperatures get high and off again when they lower
   * This is used to power an inline fan which pulls cooler air from outside to the front of my HP Microserver
 * If there is no movement in a room turn off any TP Link Smart socket which is drawing power and send an alert
   * Aim to ensure various appliances aren't left on accidentally
   * This ensures smart switches aren't turned off just because they are on, only when something connected to them is drawing power

 ## Home Assistant Resource Usage Alerts
  * Monitor system resources and send alters to specific IOS device when thresholds breached. Items monitored:
    * High Load Average
    * Low Disk Space
    * Low Memory

 # Shell Scripts
 The following scripts are stored in the `bin` directory and defined in [`shell_commands.yaml`](../shell_commands.yaml):
  * [`git_pull.sh`](../bin/git_pull.sh) - <add desc>
  * [`hass_update.sh`](../bin/hass_update.sh) - <add desc>
  * [`os_update.sh`](../bin/os_update.sh) - <add desc>
  * [`reboot.sh`](../bin/reboot.sh) - <add desc>

 # Home Assistant Scripts
 The [`scripts.yaml`](../scripts.yaml) defines how Home Assistant can call out to shell scripts. The following scripts are implemented:
  * get_latest_config - Pulls the latest changes from github then restarts home assistant
  * update_hass - Updates Home Assistant to the latest version (via `git_pull.sh`) and restarts it
  * update_os - (Not working, insufficient permissions) Update OS and then reboot system
  * update_all - (Not working, insufficient permissions) OS Update, Home Assistant Update followed by rebooting the system