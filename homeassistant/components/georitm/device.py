from homeassistant.components.georitm.georitm_api import GeoRitmObjectApi
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant


class GeoRitmDevice:
    device: GeoRitmObjectApi

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the device."""
        self.hass: HomeAssistant = hass
        self.config_entry: ConfigEntry = config_entry
        self.available: bool = True

    @property
    def name(self) -> str:
        """Return the name of this device."""
        return self.config_entry.data[CONF_NAME]

    @property
    def host(self) -> str:
        """Return the host of this device."""
        return self.config_entry.data[CONF_HOST]

    @property
    def username(self) -> str:
        """Return the username of this device."""
        return self.config_entry.data[CONF_USERNAME]

    @property
    def password(self) -> str:
        """Return the password of this device."""
        return self.config_entry.data[CONF_PASSWORD]

    async def async_setup(self) -> None:
        self.device = get_device(
            self.hass,
            host=self.config_entry.data[CONF_HOST],
            username=self.config_entry.data[CONF_USERNAME],
            password=self.config_entry.data[CONF_PASSWORD],
        )


def get_device(
    hass: HomeAssistant,
    host: str,
    username: str,
    password: str,
) -> GeoRitmObjectApi:
    return GeoRitmObjectApi(
        host=host,
        username=username,
        password=password,
    )
