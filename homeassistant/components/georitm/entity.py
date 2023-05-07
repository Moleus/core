from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)


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
        self._state = False
        self._name = f"{obj.name}: Охрана"
        self._attributes = {"deviceId": self.obj.id}
        self._attr_unique_id = f"{self.obj.id}_{self.obj.name}"

    @property
    def name(self):
        """Return the name."""
        return self._name

    def get_available(self):
        return self.obj.objectState.isOnline == 1 if self.obj else False

    @property
    def available(self):
        """Return true if device is online."""
        return self.get_available()

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self._attributes

    @property
    def obj(self) -> GeoRitmObject:
        """Return coordinator data for this entity."""
        return self.coordinator.data[self._idx]