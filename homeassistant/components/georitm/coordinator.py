"""Contains the shared Coordinator for Starlink systems."""
from __future__ import annotations

from datetime import timedelta
import logging

from aiohttp import ClientResponseError
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import GeoRitmObjecsTree
from .georitm_api import GeoRitmObjectApi

_LOGGER = logging.getLogger(__name__)


class GeoRitmUpdateCoordinator(DataUpdateCoordinator[GeoRitmObjecsTree]):
    def __init__(self, hass: HomeAssistant, name: str, api: GeoRitmObjectApi) -> None:
        self._api = api
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self) -> GeoRitmObjecsTree:
        async with async_timeout.timeout(4):
            try:
                return await self._api.fetch_objects_tree()
            except ClientResponseError as e:
                raise UpdateFailed from e

    async def async_reboot_starlink(self):
        """Reboot the Starlink system tied to this coordinator."""
        pass
        # async with async_timeout.timeout(4):
