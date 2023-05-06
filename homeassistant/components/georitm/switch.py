from typing import Any
from homeassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SwitchEntity,
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
        [
            GeoRitmSwitchEntity(coordinator, obj, idx)
            for idx, obj in enumerate(objects)
            if obj.objType == 1
        ]
    )


class GeoRitmSwitchEntity(GeoRitmDevice, SwitchEntity):
    """A SwitchEntity for Starlink devices. Handles creating unique IDs."""

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        return self._obj.objectState.isGuarded

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Arm object."""
        if not self._obj.areas:
            return False
        area = self._obj.areas[0].num
        imei = self._obj.devices[0].imei
        return await self._coordinator.async_arm(area, imei)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disarm object."""
        if not self._obj.areas:
            return False
        area = self._obj.areas[0].num
        imei = self._obj.devices[0].imei
        return await self._coordinator.async_disarm(area, imei)
