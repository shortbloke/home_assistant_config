"""Constants for Argon40."""

NAME = "Argon40"
DOMAIN = "argon40"
VERSION = "0.0.4"

ATTR_SPEED_NAME = "speed"
SERVICE_SET_FAN_SPEED = "set_fan_speed"

ATTR_ALWAYS_ON_NAME = "always_on"
SERVICE_SET_MODE = "set_mode"

ISSUE_URL = "https://github.com/Misiu/argon40/issues"
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
