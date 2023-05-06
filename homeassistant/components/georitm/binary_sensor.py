from homeassistant.components.binary_sensor import (
    DOMAIN as BINARY_DOMAIN,
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)


from .const import DOMAIN
from .model import GeoRitmObject, GeoRitmObjectsTree
from .coordinator import GeoRitmUpdateCoordinator
from .entity import GeoRitmDevice


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add cover for passed config_entry in HA."""
    coordinator: GeoRitmUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    objects: list[GeoRitmObject] = coordinator.data.objs

    async_add_entities(
        [GeoRITMGuardSensor(coordinator, obj, idx) for idx, obj in enumerate(objects)]
    )


class GeoRITMGuardSensor(GeoRitmDevice, BinarySensorEntity):
    """Representation of a GeoRITM guard binary sensor."""

    def get_state(self):
        if self._obj:
            return not self._obj.objectState.isGuarded
        return False

    @property
    def unique_id(self):
        return f"{BINARY_DOMAIN}.{DOMAIN}_{self._obj_id}_guard"

    @property
    def device_class(self):
        return BinarySensorDeviceClass.SAFETY

    @property
    def is_on(self):
        self._state = self.get_state()
        return self._state

    @property
    def icon(self):
        return "mdi:lock-open-outline" if self._state else "mdi:lock"

    @property
    def force_update(self):
        return True

    @property
    def state_attributes(self):
        return {}

    @property
    def supported_features(self):
        return 0
