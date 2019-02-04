# Configuration Validation

TravisCI is linked to this github repository, monitoring for changes and automatically validating changes against the latest version of Home Assistant. As per [Configuration file testing](https://home-assistant.io/docs/ecosystem/backup/backup_github/#step-7-configuration-file-testing)

The Travis configuration file [`.travis.yml`](../.travis.yml) defines the information needed by TravisCI. 

- Specifically the version of Python to use, currently 3.4
- The steps to perform ahead of the test such as copying files that are needed, but aren't part of the repository:
  - `travis/travis_secrets.yaml` - Contains dummy values for the secrets used in the configuration files
  - `travis/travis.fake_ssl_key` and `travis.fake_ssl_crt` - Are dummy files needed for a Home Assistant configuration setup to use SSL. Copying a fake `secrets.yanl` and some fake file for the SSL keys.
- What to install in to the test environment, i.e. homeassistant
- Define the command to run which checks the configuration: `hass -c . --script check_config`

 There is an automation script which monitors for a successful Travis build to occur, then calls the [Git Pull](https://www.home-assistant.io/addons/git_pull/) Hassio Add-On, to update the current configuration, then restart Home Assistant. Enabling changes to be made away from the Pi/HASS Hub, uploaded to GitHub and directly applied to the running system.
