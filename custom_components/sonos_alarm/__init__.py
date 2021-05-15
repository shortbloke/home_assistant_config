"""Support to embed Sonos Alarm."""
import asyncio

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID, ATTR_TIME, CONF_HOSTS
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.core import callback

from .const import DOMAIN

CONF_ADVERTISE_ADDR = "advertise_addr"
CONF_INTERFACE_ADDR = "interface_addr"

ATTR_VOLUME = "volume"
ATTR_INCLUDE_LINKED_ZONES = "include_linked_zones"


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                SWITCH_DOMAIN: vol.Schema(
                    {
                        vol.Optional(CONF_ADVERTISE_ADDR): cv.string,
                        vol.Optional(CONF_INTERFACE_ADDR): cv.string,
                        vol.Optional(CONF_HOSTS): vol.All(
                            cv.ensure_list_csv, [cv.string]
                        ),
                    }
                )
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the Sonos component."""
    conf = config.get(DOMAIN)

    hass.data[DOMAIN] = conf or {}

    if conf is not None:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_IMPORT}
            )
        )

    return True


async def async_setup_entry(hass, entry):
    """Set up Sonos from a config entry."""
    for domain in [SWITCH_DOMAIN]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, domain)
        )
    async_cleanup_sonos_devices(hass, entry)
    return True


@callback
def async_cleanup_sonos_devices(hass, entry):
    """Clean up old and invalid devices from the registry."""
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    device_entries = hass.helpers.device_registry.async_entries_for_config_entry(
        device_registry, entry.entry_id
    )

    for device_entry in device_entries:
        if (
                len(
                    hass.helpers.entity_registry.async_entries_for_device(
                        entity_registry, device_entry.id, include_disabled_entities=True
                    )
                )
                == 0
        ):
            device_registry.async_remove_device(device_entry.id)