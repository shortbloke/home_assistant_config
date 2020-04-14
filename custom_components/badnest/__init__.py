"""The example integration."""
import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from datetime import datetime
import time
from homeassistant.util.dt import utcnow

from homeassistant.const import (
    ATTR_ENTITY_ID
)

from .api import NestAPI
from .const import DOMAIN, CONF_ISSUE_TOKEN, CONF_COOKIE, CONF_USER_ID, CONF_ACCESS_TOKEN, CONF_REGION

SERVICE_BOOST_HOT_WATER = "boost_hot_water"
ATTR_TIME_PERIOD = "time_period"
ATTR_MODE = "on_off"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            {
                vol.Required(CONF_USER_ID, default=""): cv.string,
                vol.Required(CONF_ACCESS_TOKEN, default=""): cv.string,
                vol.Optional(CONF_REGION, default="us"): cv.string,
            },
            {
                vol.Required(CONF_ISSUE_TOKEN, default=""): cv.string,
                vol.Required(CONF_COOKIE, default=""): cv.string,
                vol.Optional(CONF_REGION, default="us"): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

BOOST_HOT_WATER_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_ENTITY_ID): cv.entity_id,
        vol.Optional(ATTR_TIME_PERIOD, default=30): cv.positive_int,
        vol.Required(ATTR_MODE): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the badnest component."""
    def hot_water_boost(service):
        """Handle the service call."""
        node_id = hass.data.get(service.data[ATTR_ENTITY_ID])
        if not node_id:
            # log or raise error
            _LOGGER.error("Cannot boost entity id entered")
            return

        minutes = service.data[ATTR_TIME_PERIOD]
        timeToEnd = int(time.mktime(datetime.timetuple(utcnow()))+(minutes*60))

        mode = service.data[ATTR_MODE]

        if mode == "on":
            api.hotwater_set_boost(node_id, timeToEnd)
        elif mode == "off":
            api.hotwater_set_boost(node_id, 0)

    if config.get(DOMAIN) is not None:
        user_id = config[DOMAIN].get(CONF_USER_ID)
        access_token = config[DOMAIN].get(CONF_ACCESS_TOKEN)
        issue_token = config[DOMAIN].get(CONF_ISSUE_TOKEN)
        cookie = config[DOMAIN].get(CONF_COOKIE)
        region = config[DOMAIN].get(CONF_REGION)
    else:
        email = None
        password = None
        issue_token = None
        cookie = None
        region = None

    hass.data[DOMAIN] = {
        'api': NestAPI(
            user_id,
            access_token,
            issue_token,
            cookie,
            region,
        ),
    }

    api = hass.data[DOMAIN]['api']

    hass.services.register(
        DOMAIN,
        SERVICE_BOOST_HOT_WATER,
        hot_water_boost,
        schema=BOOST_HOT_WATER_SCHEMA,
    )

    return True