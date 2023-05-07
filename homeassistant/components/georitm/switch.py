from typing import Any
from homeassistant.components.switch import (
    SwitchEntity,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .model import GeoRitmObject
from .coordinator import GeoRitmUpdateCoordinator
from .entity import GeoRitmDevice


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add cover for passed config_entry in HA."""
    coordinator: GeoRitmUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    objects: list[GeoRitmObject] = coordinator.data

    async_add_entities(
        [
            GeoRitmSwitchEntity(coordinator, obj, idx)
            for idx, obj in enumerate(objects)
            if int(obj.objType) == 1
        ]
    )


class GeoRitmSwitchEntity(GeoRitmDevice, SwitchEntity):
    """A SwitchEntity for Starlink devices. Handles creating unique IDs."""

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        return self.obj.objectState.isGuarded

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Arm object."""
        if not self.obj.areas:
            return False
        area = self.obj.areas[1].num
        imei = self.obj.devices[0].imei
        await self.coordinator.async_arm(area, imei)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disarm object."""
        if not self.obj.areas:
            return False
        area = self.obj.areas[1].num
        imei = self.obj.devices[0].imei
        await self.coordinator.async_disarm(area, imei)
        await self.coordinator.async_request_refresh()