"""Provides support for Nest cameras."""
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

SUPPORT_CHIME = 4

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass,
                               config,
                               async_add_entities,
                               discovery_info=None):
    """Set up a Nest Camera."""
    api = hass.data[DOMAIN]['api']

    cameras = []
    _LOGGER.info("Adding camera sensors")
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
            "model": self._device.device_data[self._uuid]['model'],
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
        return True if self._device.device_data[self._uuid]['streaming_state'] == \
            'streaming-enabled' or \
            self._device.device_data[self._uuid]['streaming_state'] == \
            'online-disabled' else False

    @property
    def is_recording(self):
        """Return true if the device is recording."""
        return True if self._device.device_data[self._uuid]['streaming_state'] == \
            'streaming-enabled' else False

    @property
    def brand(self):
        """Return the camera brand."""
        return "Nest Labs"

    @property
    def model(self):
        """Return the camera model."""
        return self._device.device_data[self._uuid]['model']

    def turn_off(self):
        self._device.camera_turn_off(self._uuid)
        self.schedule_update_ha_state()

    def turn_on(self):
        self._device.camera_turn_on(self._uuid)
        self.schedule_update_ha_state()

    @property
    def supported_features(self):
        """Return supported features."""
        if self.supports_doorbell_chime:
            return SUPPORT_ON_OFF + SUPPORT_CHIME
        else:
            return SUPPORT_ON_OFF

    @property
    def supports_doorbell_chime(self):
        """Return if camera supports doorbell chime."""
        return self._device.device_data[self._uuid]['indoor_chime']

    def update(self):
        """Cache value from Python-nest."""
        self._device.update()

    @property
    def name(self):
        """Return the name of this camera."""
        return self._device.device_data[self._uuid]['name']

    @property
    def state_attributes(self):
        """Return the camera state attributes."""
        attrs = {"access_token": self.access_tokens[-1]}

        if self.model:
            attrs["model_name"] = self.model

        if self.brand:
            attrs["brand"] = self.brand

        if self.motion_detection_enabled:
            attrs["motion_detection"] = self.motion_detection_enabled

        if self.supports_doorbell_chime:
            attrs["doorbell_chime"] = self.supports_doorbell_chime

        return attrs

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
