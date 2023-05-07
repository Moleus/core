"""The georitm-client integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import GeoRitmUpdateCoordinator
from .georitm_api import GeoRitmObjectApi

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up georitm-client from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create an instance of the API
    api = GeoRitmObjectApi(
        host=entry.data[CONF_HOST],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
    )

    coordinator = GeoRitmUpdateCoordinator(hass=hass, name=entry.title, api=api)

    # Validate the API connection (and authentication)
    if not await api.authenticate():
        return False

    await coordinator.async_init_devices_info()
    await coordinator.async_config_entry_first_refresh()

    # Store the API object for your platforms to access
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
