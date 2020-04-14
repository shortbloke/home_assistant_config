"""This component provides basic support for Foscam IP cameras."""
import logging
from datetime import timedelta

from homeassistant.components.camera import (
    Camera,
    SUPPORT_ON_OFF,
)
from homeassistant.util.dt import utcnow

from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass,
                               config,
                               async_add_entities,
                               discovery_info=None):
    """Set up a Nest Camera."""
    api = hass.data[DOMAIN]['api']

    cameras = []
    _LOGGER.info("Adding temperature sensors")
    for camera in api['cameras']:
        _LOGGER.info(f"Adding nest camera uuid: {camera}")
        cameras.append(NestCamera(camera, api))

    async_add_entities(cameras)


class NestCamera(Camera):
    """An implementation of a Nest camera."""

    def __init__(self, uuid, api):
        """Initialize a Nest camera."""
        super().__init__()
        self._uuid = uuid
        self._device = api
        self._time_between_snapshots = timedelta(seconds=30)
        self._last_image = None
        self._next_snapshot_at = None

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._uuid)},
            "name": self._device.device_data[self._uuid]['name'],
            "manufacturer": "Nest Labs",
            "model": "Camera",
        }

    @property
    def should_poll(self):
        return True

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self._uuid

    @property
    def is_on(self):
        """Return true if on."""
        return self._device.device_data[self._uuid]['is_online']

    @property
    def is_recording(self):
        return True
        """Return true if the device is recording."""
        return self._device.device_data[self._uuid]['is_streaming']

    def turn_off(self):
        self._device.camera_turn_off(self._uuid)
        self.schedule_update_ha_state()

    def turn_on(self):
        self._device.camera_turn_on(self._uuid)
        self.schedule_update_ha_state()

    @property
    def supported_features(self):
        """Return supported features."""
        return SUPPORT_ON_OFF

    def update(self):
        """Cache value from Python-nest."""
        self._device.update()

    @property
    def name(self):
        """Return the name of this camera."""
        return self._device.device_data[self._uuid]['name']

    def _ready_for_snapshot(self, now):
        return self._next_snapshot_at is None or now > self._next_snapshot_at

    def camera_image(self):
        """Return a still image response from the camera."""
        now = utcnow()
        if self._ready_for_snapshot(now) or True:
            image = self._device.camera_get_image(self._uuid, now)

            self._next_snapshot_at = now + self._time_between_snapshots
            self._last_image = image

        return self._last_image
