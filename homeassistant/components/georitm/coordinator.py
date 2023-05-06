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
        self._objects_info = await self._api.fetch_objects_tree()

    async def _async_update_data(self) -> GeoRitmObjectsTree:
        async with async_timeout.timeout(4):
            try:
                objects = []
                for obj in self._objects_info:
                await self._api.get_device(obj.id)
            except ClientResponseError as e:
                raise UpdateFailed from e

    async def async_arm(self, area: int, imei: str):
        """Set whether Starlink system tied to this coordinator should be stowed."""
        async with async_timeout.timeout(4):
            try:
                return await self._api.arm_object(area, imei)
            except ClientResponseError as e:
                raise UpdateFailed from e

    async def async_disarm(self, area: int, imei: str):
        """Set whether Starlink system tied to this coordinator should be stowed."""
        async with async_timeout.timeout(4):
            try:
                return await self._api.disarm_object(area, imei)
            except ClientResponseError as e:
                raise UpdateFailed from e
