import logging
from typing import Any

import aiohttp
from aiohttp import ClientResponseError

from .const import GeoRitmObjecsTree, GeoRitmObject

_LOGGER = logging.getLogger(__name__)

CORE_GEO_RITM_BASE_URL = "https://core.geo.ritm.ru/restapi"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Content-Type": "application/json",
}
# GROUP_TYPES = [0, 1]
GROUP_TYPE = 1


class GeoRitmObjectApi:
    """Class to interface with the GeoRitm API."""

    def __init__(self, host: str, username: str, password: str):
        """Initialize the API object."""
        self._host = host
        self._username = username
        self._password = password
        self._session = aiohttp.ClientSession(raise_for_status=True)
        self._headers = DEFAULT_HEADERS
        self._devices: list[GeoRitmObject] = []

    async def _post_request(
        self, session: aiohttp.ClientSession, url, data
    ) -> dict[str, Any]:
        async with session.post(url, headers=self._headers, json=data) as response:
            return await response.json()

    async def authenticate(self) -> bool:
        """Authenticate with the API."""
        # Construct the login data
        login_data = {
            "login": self._username,
            "password": self._password,
        }

        url = f"{CORE_GEO_RITM_BASE_URL}/users/login/"
        try:
            data = await self._post_request(self._session, url, login_data)
        except ClientResponseError as e:
            _LOGGER.error(
                "Couldn't authenticate using the provided credentials!: %s", e
            )
            return False

        if "basic" in data:
            self._session.headers.update({"Authorization": f"Basic {data['basic']}"})
            return True
        return False

    async def fetch_objects_tree(self) -> GeoRitmObjecsTree:
        objects_data = {"sort": "name", "groupType": GROUP_TYPE}

        try:
            objects_tree_json = await self._post_request(
                self._session,
                f"{CORE_GEO_RITM_BASE_URL}/objects/objects-tree-set/",
                objects_data,
            )
            return GeoRitmObjecsTree(**objects_tree_json)
        except ClientResponseError as e:
            if e.status == 401:
                await self.authenticate()
            raise e

    async def get_device(self, device_id) -> GeoRitmObject | None:
        url = f"{CORE_GEO_RITM_BASE_URL}/objects/obj/"
        data = {"objectId": [device_id]}

        response = await self._post_request(self._session, url, data)

        return GeoRitmObject(**response)
