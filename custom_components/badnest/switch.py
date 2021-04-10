"""Component to interface with switches that can be controlled remotely."""
import logging
from .const import DOMAIN
from homeassistant.components.switch import (
    DEVICE_CLASS_SWITCH,
)

try:
    from homeassistant.components.switch import SwitchEntity
except ImportError:
    from homeassistant.components.switch import SwitchDevice as SwitchEntity

_LOGGER = logging.getLogger(__name__)

CHIME_ON_ICON = "mdi:bell-outline"
CHIME_OFF_ICON = "mdi:bell-off-outline"


async def async_setup_platform(hass,
                               config,
                               async_add_entities,
                               discovery_info=None):
    """Create the switches for the Nest devices."""
    api = hass.data[DOMAIN]['api']
    switches = []
    _LOGGER.info("Adding switches")

    for switch in api["switches"]:
        if api.device_data[switch]['indoor_chime']:
            _LOGGER.info(f"Adding Nest Chime Switch uuid: {switch}")
            switches.append(ChimeSwitch(switch, api))

    async_add_entities(switches)


class ChimeSwitch(SwitchEntity):

    """
    Switch to turn the Nest Hello doorbell cameras indoor chime on or off.
    """

    def __init__(self, device_id, api):
        """Initialize the switch for a Nest Doorbell."""
        self.device_id = device_id
        self.device = api

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self.device_id + '_' + self.device_class

    @property
    def name(self):
        """Name of the device."""
        return self.device.device_data[self.device_id]['name'] + '_' + self.device_class

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        cs = self.device.device_data[self.device_id]['chime_state']
        return cs

    def turn_on(self, **kwargs):
        """Turn the chime on."""
        self.device.camera_turn_chime_on(self.device_id)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the chime off."""
        self.device.camera_turn_chime_off(self.device_id)
        self.schedule_update_ha_state()

    def supports_doorbell_chime(self):
        """Return if camera supports doorbell chime."""
        return self.device.device_data[self.device_id]['indoor_chime']

    @property
    def icon(self):
        """Return the icon."""
        return CHIME_ON_ICON if self.is_on else CHIME_OFF_ICON

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_SWITCH

    def update(self):
        """Get the latest data for the Switch and updates the states."""
        self.device.update()
