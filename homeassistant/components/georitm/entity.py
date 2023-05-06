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


class GeoRitmDevice(CoordinatorEntity[GeoRitmObjectsTree], Entity):
    """Representation of a GeoRITM entity."""

    def __init__(
        self, coordinator: GeoRitmUpdateCoordinator, obj: GeoRitmObject, idx: int
    ):
        """Initialize the device."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        self._coordinator = coordinator
        self._obj_id = obj.id
        self._obj: GeoRitmObject = obj
        self._name = f"{obj.name}: Охрана"
        self._state = obj.objectState.isOnline
        self._attributes = {"deviceId": self._obj_id}
        self._attr_unique_id = f"{self._coordinator.data.id}_{obj.name}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # self._attr_is_on = self._coordinator.data. [self.idx]["state"]
        current_object = self._coordinator.data.objs[self._idx]
        self._obj = current_object
        self._state = not current_object.objectState.isGuarded
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name."""
        return self._name

    def get_available(self):
        return self._obj.objectState.isOnline == 1 if self._obj else False

    @property
    def available(self):
        """Return true if device is online."""
        return self.get_available()

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self._attributes
