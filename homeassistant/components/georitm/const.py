"""Constants for the georitm-client integration."""

import logging

from homeassistant.const import Platform

DOMAIN = "georitm"
LOGGER = logging.getLogger(__package__)


CONF_HOST = "host"
CONF_LOGIN = "login"
CONF_PASSWORD = "password"

COORDINATOR_UPDATE_INTERVAL_SEC = 10
PLATFORMS = [Platform.BINARY_SENSOR]
