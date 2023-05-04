from homeassistant.components.binary_sensor import (
    DOMAIN,
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as GEORITM_DOMAIN, GeoRitmObject
from .coordinator import GeoRitmUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add cover for passed config_entry in HA."""
    coordinator: GeoRitmUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    objects: list[GeoRitmObject] = coordinator.data.objs

    async_add_entities(
        [
            GeoRITMGuardSensor(coordinator, object, idx)
            for idx, object in enumerate(objects)
        ]
    )
    # # Add all entities to HA
    # async_add_entities(GeoRITMDevice(roller) for roller in api.)


class GeoRITMDevice(Entity):
    """Representation of a GeoRITM entity."""

    def __init__(self, coordinator: GeoRitmUpdateCoordinator, obj: GeoRitmObject):
        """Initialize the device."""
        self._coordinator = coordinator
        self._obj_id = obj.id
        self._obj: GeoRitmObject = obj
        self._name = obj.name
        self._state = obj.objectState.isOnline
        self._attributes = {"deviceId": self._obj_id}

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


class GeoRITMGuardSensor(GeoRITMDevice, BinarySensorEntity):
    """Representation of a GeoRITM guard binary sensor."""

    def __init__(
        self, coordinator: GeoRitmUpdateCoordinator, obj: GeoRitmObject, idx: int
    ):
        GeoRITMDevice.__init__(self, coordinator, obj)
        self._name = f"{obj.name}: Охрана"
        self._idx = idx

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # self._attr_is_on = self._coordinator.data. [self.idx]["state"]
        current_object = self._coordinator.data.objs[self._idx]
        self._obj = current_object
        self._state = not current_object.objectState.isGuarded
        # TODO: check that _obj is updating
        # self._attributes.update(
        #     {
        #         "objType": current_object.objType,
        #         "addressShort": current_object.addressShort,
        #         "name": current_object.name,
        #     }
        self.async_write_ha_state()

    def get_state(self):
        if self._obj:
            return not self._obj.objectState.isGuarded
        return False

    @property
    def unique_id(self):
        return f"{DOMAIN}.{GEORITM_DOMAIN}_{self._obj_id}_guard"

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
