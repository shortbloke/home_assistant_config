"""The example integration."""
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .api import NestAPI
from .const import DOMAIN, CONF_ISSUE_TOKEN, CONF_COOKIE, CONF_USER_ID, CONF_ACCESS_TOKEN, CONF_REGION

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


def setup(hass, config):
    """Set up the badnest component."""
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

    return True
