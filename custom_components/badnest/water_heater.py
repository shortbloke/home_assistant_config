import logging
import time
import voluptuous as vol

from datetime import datetime
from homeassistant.util.dt import utcnow
from homeassistant.helpers import config_validation as cv
from homeassistant.const import (
    ATTR_ENTITY_ID,
)
from homeassistant.components.water_heater import (
    STATE_OFF,
    STATE_ON,
    SUPPORT_OPERATION_MODE,
    SUPPORT_AWAY_MODE,
    ATTR_AWAY_MODE,
    ATTR_OPERATION_MODE,
    ATTR_OPERATION_LIST,
)
try:
    from homeassistant.components.water_heater import WaterHeaterEntity
except ImportError:
    from homeassistant.components.water_heater import WaterHeaterDevice as WaterHeaterEntity

from .const import (
    DOMAIN,
)

STATE_SCHEDULE = 'schedule'
SERVICE_BOOST_HOT_WATER = 'boost_hot_water'
SUPPORT_BOOST_MODE = 8
ATTR_TIME_PERIOD = 'time_period'
ATTR_BOOST_MODE_STATUS = 'boost_mode_status'
ATTR_BOOST_MODE = 'boost_mode'
ATTR_HEATING_ACTIVE = 'heating_active'
ATTR_AWAY_MODE_ACTIVE = 'away_mode_active'


SUPPORTED_FEATURES = SUPPORT_OPERATION_MODE | SUPPORT_AWAY_MODE | SUPPORT_BOOST_MODE
NEST_TO_HASS_MODE = {"schedule": STATE_SCHEDULE, "off": STATE_OFF}
HASS_TO_NEST_MODE = {STATE_SCHEDULE: "schedule", STATE_OFF: "off"}
NEST_TO_HASS_STATE = {True: STATE_ON, False: STATE_OFF}
HASS_TO_NEST_STATE = {STATE_ON: True, STATE_OFF: False}
SUPPORTED_OPERATIONS = [STATE_SCHEDULE, STATE_OFF]

BOOST_HOT_WATER_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
        vol.Optional(ATTR_TIME_PERIOD, default=30): cv.positive_int,
        vol.Required(ATTR_BOOST_MODE): cv.boolean,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass,
                               config,
                               async_add_entities,
                               discovery_info=None):
    """Set up the Nest water heater device."""
    api = hass.data[DOMAIN]['api']

    waterheaters = []
    _LOGGER.info("Adding waterheaters")
    for waterheater in api['hotwatercontrollers']:
        _LOGGER.info(f"Adding nest waterheater uuid: {waterheater}")
        waterheaters.append(NestWaterHeater(waterheater, api))
    async_add_entities(waterheaters)

    def hot_water_boost(service):
        """Handle the service call."""
        entity_ids = service.data[ATTR_ENTITY_ID]
        minutes = service.data[ATTR_TIME_PERIOD]
        timeToEnd = int(time.mktime(datetime.timetuple(utcnow()))+(minutes*60))
        mode = service.data[ATTR_BOOST_MODE]
        _LOGGER.debug('HW boost mode: {} ending: {}'.format(mode, timeToEnd))

        _waterheaters = [
            x for x in waterheaters if not entity_ids or x.entity_id in entity_ids
        ]

        for nest_water_heater in _waterheaters:
            if mode:
                nest_water_heater.turn_boost_mode_on(timeToEnd)
            else:
                nest_water_heater.turn_boost_mode_off()

    hass.services.async_register(
        DOMAIN,
        SERVICE_BOOST_HOT_WATER,
        hot_water_boost,
        schema=BOOST_HOT_WATER_SCHEMA,
    )


class NestWaterHeater(WaterHeaterEntity):

    """Representation of a Nest water heater device."""

    def __init__(self, device_id, api):
        """Initialize the sensor."""
        self._name = "Nest Hot Water Heater"
        self.device_id = device_id
        self.device = api

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self.device_id + '_hw'

    @property
    def device_info(self):
        """Return device information."""
        return {"identifiers": {(DOMAIN, self.unique_id)}, "name": self.name}

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORTED_FEATURES

    @property
    def name(self):
        """Return the name of the water heater."""
        return "{0} Hot Water".format(
            self.device.device_data[self.device_id]['name'])

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:water" if self.current_operation == STATE_SCHEDULE else "mdi:water-off"

    @property
    def state(self):
        """Return the (master) state of the water heater."""
        state = STATE_OFF
        if self.device.device_data[self.device_id]['hot_water_status']:
            state = NEST_TO_HASS_STATE[self.device.device_data[self.device_id]['hot_water_status']]
        return state

    @property
    def capability_attributes(self):
        """Return capability attributes."""
        supported_features = self.supported_features or 0

        data = {}

        if supported_features & SUPPORT_OPERATION_MODE:
            data[ATTR_OPERATION_LIST] = self.operation_list

        return data

    @property
    def state_attributes(self):
        """Return the optional state attributes."""
        data = {}

        supported_features = self.supported_features

        # Operational mode will be off or schedule
        if supported_features & SUPPORT_OPERATION_MODE:
            data[ATTR_OPERATION_MODE] = self.current_operation

        # This is, is the away mode feature turned on/off
        if supported_features & SUPPORT_AWAY_MODE:
            is_away = self.is_away_mode_on
            data[ATTR_AWAY_MODE] = STATE_ON if is_away else STATE_OFF

        # away_mode_active - true if away mode is active.
        # If away mode is on, and no one has been seen for 48hrs away mode
        # should go active
        if supported_features & SUPPORT_AWAY_MODE:
            if self.device.device_data[self.device_id]['hot_water_away_active']:
                away_active = self.device.device_data[self.device_id]['hot_water_away_active']
                data[ATTR_AWAY_MODE_ACTIVE] = away_active
            else:
                data[ATTR_AWAY_MODE_ACTIVE] = False

        if supported_features & SUPPORT_BOOST_MODE:
            # boost_mode - true if boost mode is currently active.
            # boost_mode will be 0 if off, and non-zero otherwise - it is set to
            # the epoch time when the boost is due to end
            if self.device.device_data[self.device_id]['hot_water_boost_setting']:
                boost_mode = self.device.device_data[self.device_id]['hot_water_boost_setting']
                data[ATTR_BOOST_MODE_STATUS] = bool(boost_mode)
            else:
                data[ATTR_BOOST_MODE_STATUS] = False

        # heating_active - true if hot water is currently being heated.
        # So it is either on via schedule or boost and currently firing
        # (demand on) the boiler
        if self.device.device_data[self.device_id]['hot_water_status']:
            if self.device.device_data[self.device_id]['hot_water_actively_heating']:
                boiler_firing = self.device.device_data[self.device_id]['hot_water_actively_heating']
                data[ATTR_HEATING_ACTIVE] = boiler_firing
            else:
                data[ATTR_HEATING_ACTIVE] = False
        else:
            data[ATTR_HEATING_ACTIVE] = False

        _LOGGER.debug("Device state attributes: {}".format(data))
        return data

    @property
    def current_operation(self):
        """Return current operation ie. eco, electric, performance, ..."""
        return NEST_TO_HASS_MODE[self.device.device_data[self.device_id]['hot_water_timer_mode']]

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return SUPPORTED_OPERATIONS

    @property
    def is_away_mode_on(self):
        """Return true if away mode is on."""
        away = self.device.device_data[self.device_id]['hot_water_away_setting']
        return away

    def set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        if self.device.device_data[self.device_id]['has_hot_water_control']:
            self.device.hotwater_set_mode(self.device_id, mode=operation_mode)

    async def async_set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        await self.hass.async_add_executor_job(self.set_operation_mode, operation_mode)

    def turn_away_mode_on(self):
        """Turn away mode on."""
        if self.device.device_data[self.device_id]['has_hot_water_control']:
            self.device.hotwater_set_away_mode(self.device_id, away_mode=True)

    async def async_turn_away_mode_on(self):
        """Turn away mode on."""
        await self.hass.async_add_executor_job(self.turn_away_mode_on)

    def turn_away_mode_off(self):
        """Turn away mode off."""
        if self.device.device_data[self.device_id]['has_hot_water_control']:
            self.device.hotwater_set_away_mode(self.device_id, away_mode=False)

    async def async_turn_away_mode_off(self):
        """Turn away mode off."""
        await self.hass.async_add_executor_job(self.turn_away_mode_off)

    def turn_boost_mode_on(self, timeToEnd):
        """Turn boost mode on."""
        if self.device.device_data[self.device_id]['has_hot_water_control']:
            self.device.hotwater_set_boost(self.device_id, time=timeToEnd)

    def turn_boost_mode_off(self):
        """Turn boost mode off."""
        if self.device.device_data[self.device_id]['has_hot_water_control']:
            self.device.hotwater_set_boost(self.device_id, time=0)

    def update(self):
        """Get the latest data from the Hot Water Sensor and updates the states."""
        self.device.update()


async def async_service_away_mode(entity, service):
    """Handle away mode service."""
    if service.data[ATTR_AWAY_MODE]:
        await entity.async_turn_away_mode_on()
    else:
        await entity.async_turn_away_mode_off()
