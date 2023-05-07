"""Contains the shared Coordinator for Starlink systems."""
from __future__ import annotations

from datetime import timedelta
import logging

from aiohttp import ClientResponseError
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .model import GeoRitmObjectsTree, GeoRitmObject
from .georitm_api import GeoRitmObjectApi
from .const import COORDINATOR_UPDATE_INTERVAL_SEC

_LOGGER = logging.getLogger(__name__)


class GeoRitmUpdateCoordinator(DataUpdateCoordinator[GeoRitmObjectsTree]):
    def __init__(self, hass: HomeAssistant, name: str, api: GeoRitmObjectApi) -> None:
        self._objects_info: list[GeoRitmObject]
        self._api = api
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=COORDINATOR_UPDATE_INTERVAL_SEC),
        )

    async def async_init_devices_info(self):
        tree = await self._api.fetch_objects_tree()
        self._objects_info = tree.objs

    async def _async_update_data(self) -> list[GeoRitmObject]:
        async with async_timeout.timeout(8):
            try:
                return await self._api.fetch_full_objects(
                    list(map(lambda o: o.id, self._objects_info))
                )
            except ClientResponseError as e:
                raise UpdateFailed from e

    async def async_arm(self, area: int, imei: str):
        """Arm object"""
        async with async_timeout.timeout(4):
            try:
                return await self._api.arm_object(area, imei)
            except ClientResponseError as e:
                raise UpdateFailed from e

    async def async_disarm(self, area: int, imei: str):
        """Disarm object"""
        async with async_timeout.timeout(4):
            try:
                return await self._api.disarm_object(area, imei)
            except ClientResponseError as e:
                raise UpdateFailed from e
