import logging

import requests

API_URL = "https://home.nest.com"
CAMERA_WEBAPI_BASE = "https://webapi.camera.home.nest.com"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/75.0.3770.100 Safari/537.36"
URL_JWT = "https://nestauthproxyservice-pa.googleapis.com/v1/issue_jwt"

# Nest website's (public) API key
NEST_API_KEY = "AIzaSyAdkSIMNc51XGNEAYWasX9UOWkS5P6sZE4"

KNOWN_BUCKET_TYPES = [
    # Thermostats
    "device",
    "shared",
    # Protect
    "topaz",
    # Temperature sensors
    "kryptonite",
]

_LOGGER = logging.getLogger(__name__)


class NestAPI():
    def __init__(self,
                 user_id,
                 access_token,
                 issue_token,
                 cookie,
                 region):
        """
        Initialize the device.

        Args:
            self: (todo): write your description
            user_id: (str): write your description
            access_token: (str): write your description
            issue_token: (str): write your description
            cookie: (todo): write your description
            region: (str): write your description
        """
        self.device_data = {}
        self._wheres = {}
        self._user_id = user_id
        self._access_token = access_token
        self._session = requests.Session()
        self._session.headers.update({
            "Referer": "https://home.nest.com/",
            "User-Agent": USER_AGENT,
        })
        self._issue_token = issue_token
        self._cookie = cookie
        self._czfe_url = None
        self._camera_url = f'https://nexusapi-{region}1.camera.home.nest.com'
        self.cameras = []
        self.thermostats = []
        self.temperature_sensors = []
        self.hotwatercontrollers = []
        self.protects = []
        self.login()
        self._get_devices()
        self.update()

    def __getitem__(self, name):
        """
        Get an attribute by name.

        Args:
            self: (todo): write your description
            name: (str): write your description
        """
        return getattr(self, name)

    def __setitem__(self, name, value):
        """
        Sets an item.

        Args:
            self: (todo): write your description
            name: (str): write your description
            value: (str): write your description
        """
        return setattr(self, name, value)

    def __delitem__(self, name):
        """
        Removes an item from the cache.

        Args:
            self: (todo): write your description
            name: (str): write your description
        """
        return delattr(self, name)

    def __contains__(self, name):
        """
        Return true if the given name contains a given name.

        Args:
            self: (todo): write your description
            name: (str): write your description
        """
        return hasattr(self, name)

    def login(self):
        """
        Perform a github login.

        Args:
            self: (todo): write your description
        """
        if self._issue_token and self._cookie:
            self._login_google(self._issue_token, self._cookie)
        self._login_dropcam()

    def _login_google(self, issue_token, cookie):
        """
        Login to github.

        Args:
            self: (todo): write your description
            issue_token: (str): write your description
            cookie: (todo): write your description
        """
        headers = {
            'User-Agent': USER_AGENT,
            'Sec-Fetch-Mode': 'cors',
            'X-Requested-With': 'XmlHttpRequest',
            'Referer': 'https://accounts.google.com/o/oauth2/iframe',
            'cookie': cookie
        }
        r = self._session.get(url=issue_token, headers=headers)
        access_token = r.json()['access_token']

        headers = {
            'User-Agent': USER_AGENT,
            'Authorization': 'Bearer ' + access_token,
            'x-goog-api-key': NEST_API_KEY,
            'Referer': 'https://home.nest.com'
        }
        params = {
            "embed_google_oauth_access_token": True,
            "expire_after": '3600s',
            "google_oauth_access_token": access_token,
            "policy_id": 'authproxy-oauth-policy'
        }
        r = self._session.post(url=URL_JWT, headers=headers, params=params)
        self._user_id = r.json()['claims']['subject']['nestId']['id']
        self._access_token = r.json()['jwt']

    def _login_dropcam(self):
        """
        Login to the session.

        Args:
            self: (todo): write your description
        """
        self._session.post(
            f"{API_URL}/dropcam/api/login",
            data={"access_token": self._access_token}
        )

    def _get_cameras(self):
        """
        Return a list of camera addresses.

        Args:
            self: (todo): write your description
        """
        cameras = []

        try:
            r = self._session.get(
                f"{CAMERA_WEBAPI_BASE}/api/cameras."
                + "get_owned_and_member_of_with_properties"
            )

            for camera in r.json()["items"]:
                cameras.append(camera['uuid'])
                self.device_data[camera['uuid']] = {}

            return cameras
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to get cameras, trying again')
            return self._get_cameras()
        except KeyError:
            _LOGGER.debug('Failed to get cameras, trying to log in again')
            self.login()
            return self._get_cameras()

    def _get_devices(self):
        """
        Get devices.

        Args:
            self: (todo): write your description
        """
        try:
            r = self._session.post(
                f"{API_URL}/api/0.1/user/{self._user_id}/app_launch",
                json={
                    "known_bucket_types": ["buckets"],
                    "known_bucket_versions": [],
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )

            self._czfe_url = r.json()["service_urls"]["urls"]["czfe_url"]

            buckets = r.json()['updated_buckets'][0]['value']['buckets']
            for bucket in buckets:
                if bucket.startswith('topaz.'):
                    sn = bucket.replace('topaz.', '')
                    self.protects.append(sn)
                    self.device_data[sn] = {}
                elif bucket.startswith('kryptonite.'):
                    sn = bucket.replace('kryptonite.', '')
                    self.temperature_sensors.append(sn)
                    self.device_data[sn] = {}
                elif bucket.startswith('device.'):
                    sn = bucket.replace('device.', '')
                    self.thermostats.append(sn)
                    self.temperature_sensors.append(sn)
                    self.hotwatercontrollers.append(sn)
                    self.device_data[sn] = {}

            self.cameras = self._get_cameras()

        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to get devices, trying again')
            return self.get_devices()
        except KeyError:
            _LOGGER.debug('Failed to get devices, trying to log in again')
            self.login()
            return self.get_devices()


    def _map_nest_protect_state(self, value):
        """
        Return the nest_protect_protect_state to the nest - 2. 0 - 1.

        Args:
            self: (todo): write your description
            value: (todo): write your description
        """
        if value == 0:
            return "Ok"
        elif value == 1 or value == 2:
            return "Warning"
        elif value == 3:
            return "Emergency"
        else:
            return "Unknown"

    def update(self):
        """
        Updates the device.

        Args:
            self: (todo): write your description
        """
        try:
            # To get friendly names
            r = self._session.post(
                f"{API_URL}/api/0.1/user/{self._user_id}/app_launch",
                json={
                    "known_bucket_types": ["where"],
                    "known_bucket_versions": [],
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )

            for bucket in r.json()["updated_buckets"]:
                sensor_data = bucket["value"]
                sn = bucket["object_key"].split('.')[1]
                if bucket["object_key"].startswith(
                        f"where.{sn}"):
                    wheres = sensor_data['wheres']
                    for where in wheres:
                        self._wheres[where['where_id']] = where['name']

            r = self._session.post(
                f"{API_URL}/api/0.1/user/{self._user_id}/app_launch",
                json={
                    "known_bucket_types": KNOWN_BUCKET_TYPES,
                    "known_bucket_versions": [],
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )

            for bucket in r.json()["updated_buckets"]:
                sensor_data = bucket["value"]
                sn = bucket["object_key"].split('.')[1]
                # Thermostats (thermostat and sensors system)
                if bucket["object_key"].startswith(
                        f"shared.{sn}"):
                    self.device_data[sn]['current_temperature'] = \
                        sensor_data["current_temperature"]
                    self.device_data[sn]['target_temperature'] = \
                        sensor_data["target_temperature"]
                    self.device_data[sn]['hvac_ac_state'] = \
                        sensor_data["hvac_ac_state"]
                    self.device_data[sn]['hvac_heater_state'] = \
                        sensor_data["hvac_heater_state"]
                    self.device_data[sn]['target_temperature_high'] = \
                        sensor_data["target_temperature_high"]
                    self.device_data[sn]['target_temperature_low'] = \
                        sensor_data["target_temperature_low"]
                    self.device_data[sn]['can_heat'] = \
                        sensor_data["can_heat"]
                    self.device_data[sn]['can_cool'] = \
                        sensor_data["can_cool"]
                    self.device_data[sn]['mode'] = \
                        sensor_data["target_temperature_type"]
                    if self.device_data[sn]['hvac_ac_state']:
                        self.device_data[sn]['action'] = "cooling"
                    elif self.device_data[sn]['hvac_heater_state']:
                        self.device_data[sn]['action'] = "heating"
                    else:
                        self.device_data[sn]['action'] = "off"
                # Thermostats, pt 2
                elif bucket["object_key"].startswith(
                        f"device.{sn}"):
                    self.device_data[sn]['name'] = self._wheres[
                        sensor_data['where_id']
                    ]
                    # When acts as a sensor
                    if 'backplate_temperature' in sensor_data:
                        self.device_data[sn]['temperature'] = \
                            sensor_data['backplate_temperature']
                    if 'battery_level' in sensor_data:
                        self.device_data[sn]['battery_level'] = \
                            sensor_data['battery_level']

                    if sensor_data.get('description', None):
                        self.device_data[sn]['name'] += \
                            f' ({sensor_data["description"]})'
                    self.device_data[sn]['name'] += ' Thermostat'
                    self.device_data[sn]['has_fan'] = \
                        sensor_data["has_fan"]
                    self.device_data[sn]['fan'] = \
                        sensor_data["fan_timer_timeout"]
                    self.device_data[sn]['current_humidity'] = \
                        sensor_data["current_humidity"]
                    self.device_data[sn]['target_humidity'] = \
                        sensor_data["target_humidity"]
                    self.device_data[sn]['target_humidity_enabled'] = \
                        sensor_data["target_humidity_enabled"]
                    if sensor_data["eco"]["mode"] == 'manual-eco' or \
                            sensor_data["eco"]["mode"] == 'auto-eco':
                        self.device_data[sn]['eco'] = True
                    else:
                        self.device_data[sn]['eco'] = False

                    # Hot water
                    # - Status
                    self.device_data[sn]['has_hot_water_control'] = \
                        sensor_data["has_hot_water_control"]
                    self.device_data[sn]['hot_water_status'] = \
                        sensor_data["hot_water_active"]
                    self.device_data[sn]['hot_water_actively_heating'] = \
                        sensor_data["hot_water_boiling_state"]
                    self.device_data[sn]['hot_water_away_active'] = \
                        sensor_data["hot_water_away_active"]
                    # - Status/Settings
                    self.device_data[sn]['hot_water_timer_mode'] = \
                        sensor_data["hot_water_mode"]
                    self.device_data[sn]['hot_water_away_setting'] = \
                        sensor_data["hot_water_away_enabled"]
                    self.device_data[sn]['hot_water_boost_setting'] = \
                        sensor_data["hot_water_boost_time_to_end"]

                # Protect
                elif bucket["object_key"].startswith(
                        f"topaz.{sn}"):
                    self.device_data[sn]['name'] = self._wheres[
                        sensor_data['where_id']
                    ]
                    if sensor_data.get('description', None):
                        self.device_data[sn]['name'] += \
                            f' ({sensor_data["description"]})'
                    self.device_data[sn]['name'] += ' Protect'
                    self.device_data[sn]['co_status'] = \
                        self._map_nest_protect_state(sensor_data['co_status'])
                    self.device_data[sn]['smoke_status'] = \
                        self._map_nest_protect_state(sensor_data['smoke_status'])
                    self.device_data[sn]['battery_health_state'] = \
                        self._map_nest_protect_state(sensor_data['battery_health_state'])
                # Temperature sensors
                elif bucket["object_key"].startswith(
                        f"kryptonite.{sn}"):
                    self.device_data[sn]['name'] = self._wheres[
                        sensor_data['where_id']
                    ]
                    if sensor_data.get('description', None):
                        self.device_data[sn]['name'] += \
                            f' ({sensor_data["description"]})'
                    self.device_data[sn]['name'] += ' Temperature'
                    self.device_data[sn]['temperature'] = \
                        sensor_data['current_temperature']
                    self.device_data[sn]['battery_level'] = \
                        sensor_data['battery_level']

            # Cameras
            for camera in self.cameras:
                r = self._session.get(
                    f"{API_URL}/dropcam/api/cameras/{camera}"
                )
                sensor_data = r.json()[0]
                self.device_data[camera]['name'] = \
                    sensor_data["name"]
                self.device_data[camera]['is_online'] = \
                    sensor_data["is_online"]
                self.device_data[camera]['is_streaming'] = \
                    sensor_data["is_streaming"]
                self.device_data[camera]['battery_voltage'] = \
                    sensor_data["rq_battery_battery_volt"]
                self.device_data[camera]['ac_voltage'] = \
                    sensor_data["rq_battery_vbridge_volt"]
                self.device_data[camera]['location'] = \
                    sensor_data["location"]
                self.device_data[camera]['data_tier'] = \
                    sensor_data["properties"]["streaming.data-usage-tier"]
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to update, trying again')
            self.update()
        except KeyError:
            _LOGGER.debug('Failed to update, trying to log in again')
            self.login()
            self.update()

    def thermostat_set_temperature(self, device_id, temp, temp_high=None):
        """
        Set the thermostat temperature.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
            temp: (todo): write your description
            temp_high: (todo): write your description
        """
        if device_id not in self.thermostats:
            return

        try:
            if temp_high is None:
                self._session.post(
                    f"{self._czfe_url}/v5/put",
                    json={
                        "objects": [
                            {
                                "object_key": f'shared.{device_id}',
                                "op": "MERGE",
                                "value": {"target_temperature": temp},
                            }
                        ]
                    },
                    headers={"Authorization": f"Basic {self._access_token}"},
                )
            else:
                self._session.post(
                    f"{self._czfe_url}/v5/put",
                    json={
                        "objects": [
                            {
                                "object_key": f'shared.{device_id}',
                                "op": "MERGE",
                                "value": {
                                    "target_temperature_low": temp,
                                    "target_temperature_high": temp_high,
                                },
                            }
                        ]
                    },
                    headers={"Authorization": f"Basic {self._access_token}"},
                )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set temperature, trying again')
            self.thermostat_set_temperature(device_id, temp, temp_high)
        except KeyError:
            _LOGGER.debug('Failed to set temperature, trying to log in again')
            self.login()
            self.thermostat_set_temperature(device_id, temp, temp_high)

    def thermostat_set_target_humidity(self, device_id, humidity):
        """
        : param humidity_id to target.

        Args:
            self: (todo): write your description
            device_id: (str): write your description
            humidity: (str): write your description
        """
        if device_id not in self.thermostats:
            return

        try:
            self._session.post(
                f"{self._czfe_url}/v5/put",
                json={
                    "objects": [
                        {
                            "object_key": f'device.{device_id}',
                            "op": "MERGE",
                            "value": {"target_humidity": humidity},
                        }
                    ]
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set humidity, trying again')
            self.thermostat_set_target_humidity(device_id, humidity)
        except KeyError:
            _LOGGER.debug('Failed to set humidity, trying to log in again')
            self.login()
            self.thermostat_set_target_humidity(device_id, humidity)

    def thermostat_set_mode(self, device_id, mode):
        """
        Change the thermostat mode.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
            mode: (todo): write your description
        """
        if device_id not in self.thermostats:
            return

        try:
            self._session.post(
                f"{self._czfe_url}/v5/put",
                json={
                    "objects": [
                        {
                            "object_key": f'shared.{device_id}',
                            "op": "MERGE",
                            "value": {"target_temperature_type": mode},
                        }
                    ]
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set mode, trying again')
            self.thermostat_set_mode(device_id, mode)
        except KeyError:
            _LOGGER.debug('Failed to set mode, trying to log in again')
            self.login()
            self.thermostat_set_mode(device_id, mode)

    def thermostat_set_fan(self, device_id, date):
        """
        Sets the fan fan.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
            date: (todo): write your description
        """
        if device_id not in self.thermostats:
            return

        try:
            self._session.post(
                f"{self._czfe_url}/v5/put",
                json={
                    "objects": [
                        {
                            "object_key": f'device.{device_id}',
                            "op": "MERGE",
                            "value": {"fan_timer_timeout": date},
                        }
                    ]
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set fan, trying again')
            self.thermostat_set_fan(device_id, date)
        except KeyError:
            _LOGGER.debug('Failed to set fan, trying to log in again')
            self.login()
            self.thermostat_set_fan(device_id, date)

    def thermostat_set_eco_mode(self, device_id, state):
        """
        : param thermostmost mode.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
            state: (todo): write your description
        """
        if device_id not in self.thermostats:
            return

        try:
            mode = 'manual-eco' if state else 'schedule'
            self._session.post(
                f"{self._czfe_url}/v5/put",
                json={
                    "objects": [
                        {
                            "object_key": f'device.{device_id}',
                            "op": "MERGE",
                            "value": {"eco": {"mode": mode}},
                        }
                    ]
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set eco, trying again')
            self.thermostat_set_eco_mode(device_id, state)
        except KeyError:
            _LOGGER.debug('Failed to set eco, trying to log in again')
            self.login()
            self.thermostat_set_eco_mode(device_id, state)

    def hotwater_set_boost(self, device_id, time):
        """
        : param device_boost.

        Args:
            self: (todo): write your description
            device_id: (str): write your description
            time: (todo): write your description
        """
        if device_id not in self.hotwatercontrollers:
            return

        try:
            self._session.post(
                f"{self._czfe_url}/v5/put",
                json={
                    "objects": [
                        {
                            "object_key": f'device.{device_id}',
                            "op": "MERGE",
                            "value": {"hot_water_boost_time_to_end": time},
                        }
                    ]
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to boost hot water, trying again')
            self.hotwater_set_boost(device_id, time)
        except KeyError:
            _LOGGER.debug('Failed to boost hot water, trying to log in again')
            self.login()
            self.hotwater_set_boost(device_id, time)

    def hotwater_set_away_mode(self, device_id, away_mode):
        """
        : param device_id : param hotwater.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
            away_mode: (str): write your description
        """
        if device_id not in self.hotwatercontrollers:
            return

        try:
            self._session.post(
                f"{self._czfe_url}/v5/put",
                json={
                    "objects": [
                        {
                            "object_key": f'device.{device_id}',
                            "op": "MERGE",
                            "value": {"hot_water_away_enabled": away_mode},
                        }
                    ]
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set hot water away mode, trying again')
            self.hotwater_set_away_mode(device_id, away_mode)
        except KeyError:
            _LOGGER.debug('Failed to set hot water away mode, '
                          'trying to log in again')
            self.login()
            self.hotwater_set_away_mode(device_id, away_mode)

    def hotwater_set_mode(self, device_id, mode):
        """
        Set the hotwater mode.

        Args:
            self: (todo): write your description
            device_id: (str): write your description
            mode: (str): write your description
        """
        if device_id not in self.hotwatercontrollers:
            return

        try:
            self._session.post(
                f"{self._czfe_url}/v5/put",
                json={
                    "objects": [
                        {
                            "object_key": f'device.{device_id}',
                            "op": "MERGE",
                            "value": {"hot_water_mode": mode},
                        }
                    ]
                },
                headers={"Authorization": f"Basic {self._access_token}"},
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set hot water mode, trying again')
            self.hotwater_set_boost(device_id, mode)
        except KeyError:
            _LOGGER.debug('Failed to set hot water mode, '
                          'trying to log in again')
            self.login()
            self.hotwater_set_boost(device_id, mode)

    def _camera_set_properties(self, device_id, property, value):
        """
        Set camera properties.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
            property: (str): write your description
            value: (todo): write your description
        """
        if device_id not in self.cameras:
            return

        try:
            r = self._session.post(
                f"{CAMERA_WEBAPI_BASE}/api/dropcams.set_properties",
                data={property: value, "uuid": device_id},
            )

            return r.json()["items"]
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to set camera property, trying again')
            return self._camera_set_properties(device_id, property, value)
        except KeyError:
            _LOGGER.debug('Failed to set camera property, ' +
                          'trying to log in again')
            self.login()
            return self._camera_set_properties(device_id, property, value)

    def camera_turn_off(self, device_id):
        """
        Turn a camera.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
        """
        if device_id not in self.cameras:
            return

        return self._set_properties(device_id, "streaming.enabled", "false")

    def camera_turn_on(self, device_id):
        """
        Turn camera camera camera.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
        """
        if device_id not in self.cameras:
            return

        return self._set_properties(device_id, "streaming.enabled", "true")

    def camera_get_image(self, device_id, now):
        """
        Retrieve a camera.

        Args:
            self: (todo): write your description
            device_id: (int): write your description
            now: (todo): write your description
        """
        if device_id not in self.cameras:
            return

        try:
            r = self._session.get(
                f'{self._camera_url}/get_image?uuid={device_id}' +
                f'&cachebuster={now}'
            )

            return r.content
        except requests.exceptions.RequestException as e:
            _LOGGER.error(e)
            _LOGGER.error('Failed to get camera image, trying again')
            return self.camera_get_image(device_id, now)
        except KeyError:
            _LOGGER.debug('Failed to get camera image, trying to log in again')
            self.login()
            return self.camera_get_image(device_id, now)
