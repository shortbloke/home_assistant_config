"""Demo platform that offers a fake climate device."""
from datetime import datetime
import logging

from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    FAN_AUTO,
    FAN_ON,
    HVAC_MODE_AUTO,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_FAN_MODE,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_RANGE,
    SUPPORT_TARGET_HUMIDITY,
    PRESET_ECO,
    PRESET_NONE,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_COOL,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    TEMP_CELSIUS,
)

from .const import (
    DOMAIN,
)

NEST_MODE_HEAT_COOL = "range"
NEST_MODE_ECO = "eco"
NEST_MODE_HEAT = "heat"
NEST_MODE_COOL = "cool"
NEST_MODE_OFF = "off"

MODE_HASS_TO_NEST = {
    HVAC_MODE_AUTO: NEST_MODE_HEAT_COOL,
    HVAC_MODE_HEAT: NEST_MODE_HEAT,
    HVAC_MODE_COOL: NEST_MODE_COOL,
    HVAC_MODE_OFF: NEST_MODE_OFF,
}

ACTION_NEST_TO_HASS = {
    "off": CURRENT_HVAC_IDLE,
    "heating": CURRENT_HVAC_HEAT,
    "cooling": CURRENT_HVAC_COOL,
}

MODE_NEST_TO_HASS = {v: k for k, v in MODE_HASS_TO_NEST.items()}

ROUND_TARGET_HUMIDITY_TO_NEAREST = 5
NEST_HUMIDITY_MIN = 10
NEST_HUMIDITY_MAX = 60

PRESET_MODES = [PRESET_NONE, PRESET_ECO]

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass,
                               config,
                               async_add_entities,
                               discovery_info=None):
    """Set up the Nest climate device."""
    api = hass.data[DOMAIN]['api']

    thermostats = []
    _LOGGER.info("Adding thermostats")
    for thermostat in api['thermostats']:
        _LOGGER.info(f"Adding nest thermostat uuid: {thermostat}")
        thermostats.append(NestClimate(thermostat, api))

    async_add_entities(thermostats)


class NestClimate(ClimateDevice):
    """Representation of a Nest climate device."""

    def __init__(self, device_id, api):
        """Initialize the thermostat."""
        self._name = "Nest Thermostat"
        self._unit_of_measurement = TEMP_CELSIUS
        self._fan_modes = [FAN_ON, FAN_AUTO]
        self.device_id = device_id

        # Set the default supported features
        self._support_flags = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

        # Not all nest devices support cooling and heating remove unused
        self._operation_list = []

        self.device = api

        if self.device.device_data[device_id]['can_heat'] \
                and self.device.device_data[device_id]['can_cool']:
            self._operation_list.append(HVAC_MODE_AUTO)
            self._support_flags |= SUPPORT_TARGET_TEMPERATURE_RANGE

        # Add supported nest thermostat features
        if self.device.device_data[device_id]['can_heat']:
            self._operation_list.append(HVAC_MODE_HEAT)

        if self.device.device_data[device_id]['can_cool']:
            self._operation_list.append(HVAC_MODE_COOL)

        self._operation_list.append(HVAC_MODE_OFF)

        # feature of device
        if self.device.device_data[device_id]['has_fan']:
            self._support_flags = self._support_flags | SUPPORT_FAN_MODE

        if self.device.device_data[device_id]['target_humidity_enabled']:
            self._support_flags = self._support_flags | SUPPORT_TARGET_HUMIDITY
            

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self.device_id

    @property
    def name(self):
        """Return an friendly name."""
        return self.device.device_data[self.device_id]['name']

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._support_flags

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.device.device_data[self.device_id]['current_temperature']

    @property
    def current_humidity(self):
        """Return the current humidity."""
        return self.device.device_data[self.device_id]['current_humidity']

    @property
    def target_humidity(self):
        """Return the target humidity."""
        return self.device.device_data[self.device_id]['target_humidity']
        
    @property
    def min_humidity(self):
        """Return the min target humidity."""
        return NEST_HUMIDITY_MIN

    @property
    def max_humidity(self):
        """Return the max target humidity."""
        return NEST_HUMIDITY_MAX

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        if self.device.device_data[self.device_id]['mode'] \
                != NEST_MODE_HEAT_COOL \
                and not self.device.device_data[self.device_id]['eco']:
            return \
                self.device.device_data[self.device_id]['target_temperature']
        return None

    @property
    def target_temperature_high(self):
        """Return the highbound target temperature we try to reach."""
        if self.device.device_data[self.device_id]['mode'] \
                == NEST_MODE_HEAT_COOL \
                and not self.device.device_data[self.device_id]['eco']:
            return \
                self.device. \
                device_data[self.device_id]['target_temperature_high']
        return None

    @property
    def target_temperature_low(self):
        """Return the lowbound target temperature we try to reach."""
        if self.device.device_data[self.device_id]['mode'] \
                == NEST_MODE_HEAT_COOL \
                and not self.device.device_data[self.device_id]['eco']:
            return \
                self.device. \
                device_data[self.device_id]['target_temperature_low']
        return None

    @property
    def hvac_action(self):
        """Return current operation ie. heat, cool, idle."""
        return ACTION_NEST_TO_HASS[
            self.device.device_data[self.device_id]['action']
        ]

    @property
    def hvac_mode(self):
        """Return hvac target hvac state."""
        if self.device.device_data[self.device_id]['mode'] is None \
                or self.device.device_data[self.device_id]['eco']:
            # We assume the first operation in operation list is the main one
            return self._operation_list[0]

        return MODE_NEST_TO_HASS[
            self.device.device_data[self.device_id]['mode']
        ]

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return self._operation_list

    @property
    def preset_mode(self):
        """Return current preset mode."""
        if self.device.device_data[self.device_id]['eco']:
            return PRESET_ECO

        return PRESET_NONE

    @property
    def preset_modes(self):
        """Return preset modes."""
        return PRESET_MODES

    @property
    def fan_mode(self):
        """Return whether the fan is on."""
        if self.device.device_data[self.device_id]['has_fan']:
            # Return whether the fan is on
            if self.device.device_data[self.device_id]['fan']:
                return FAN_ON
            else:
                return FAN_AUTO
        # No Fan available so disable slider
        return None

    @property
    def fan_modes(self):
        """Return the list of available fan modes."""
        if self.device.device_data[self.device_id]['has_fan']:
            return self._fan_modes
        return None

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = None
        target_temp_low = kwargs.get(ATTR_TARGET_TEMP_LOW)
        target_temp_high = kwargs.get(ATTR_TARGET_TEMP_HIGH)
        if self.device.device_data[self.device_id]['mode'] == \
                NEST_MODE_HEAT_COOL:
            if target_temp_low is not None and target_temp_high is not None:
                self.device.thermostat_set_temperature(
                    self.device_id,
                    target_temp_low,
                    target_temp_high,
                )
        else:
            temp = kwargs.get(ATTR_TEMPERATURE)
            if temp is not None:
                self.device.thermostat_set_temperature(
                    self.device_id,
                    temp,
                )

    def set_humidity(self, humidity):
        """Set new target humidity."""
        humidity = int(round(float(humidity) / ROUND_TARGET_HUMIDITY_TO_NEAREST) * ROUND_TARGET_HUMIDITY_TO_NEAREST)
        if humidity < NEST_HUMIDITY_MIN:
            humidity = NEST_HUMIDITY_MIN
        if humidity > NEST_HUMIDITY_MAX:
            humidity = NEST_HUMIDITY_MAX
        self.device.thermostat_set_target_humidity(
            self.device_id,
            humidity,
        )

    def set_hvac_mode(self, hvac_mode):
        """Set operation mode."""
        self.device.thermostat_set_mode(
            self.device_id,
            MODE_HASS_TO_NEST[hvac_mode],
        )

    def set_fan_mode(self, fan_mode):
        """Turn fan on/off."""
        if self.device.device_data[self.device_id]['has_fan']:
            if fan_mode == "on":
                self.device.thermostat_set_fan(
                    self.device_id,
                    int(datetime.now().timestamp() + 60 * 30),
                )
            else:
                self.device.thermostat_set_fan(
                    self.device_id,
                    0,
                )

    def set_preset_mode(self, preset_mode):
        """Set preset mode."""
        need_eco = preset_mode == PRESET_ECO

        if need_eco != self.device.device_data[self.device_id]['eco']:
            self.device.thermostat_set_eco_mode(
                self.device_id,
                need_eco,
            )

    def update(self):
        """Updates data"""
        self.device.update()
