# Additional Info
Private information is stored in secrets.yaml (not uploaded)

# Config updating and validation
 - Changes to configuration are pushed to git using `gitupdate.sh` script.
 - TravisCI is connected to this repository, which will run a script validation for each check-in automatically. Setup as per: https://home-assistant.io/docs/ecosystem/backup/backup_github/
   - Note in order for Travis to work a number of extra files are required:
     - `travis/travis_secrets.yaml` - Contains dummy values for the secrets used in the configuration files
     - `travis/travis.fake_ssl_key` and `travis.fake_ssl_crt` - Are dummy files needed for a Home Assistant configuration setup to use SSL.
 - A successful Travis build triggers a git pull request to update the current configuration, followed by restarting the home assistant service. Enabling changes to be made away from the the Pi/HASS Hub, uploaded to GitHub and directly applied to the running system.