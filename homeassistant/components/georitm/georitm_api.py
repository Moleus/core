import logging
from typing import Any
from dacite import from_dict

import aiohttp
from aiohttp import ClientResponseError

from .model import GeoRitmObjectsTree, GeoRitmObject, ObjArea

_LOGGER = logging.getLogger(__name__)

CORE_GEO_RITM_BASE_URL = "https://core.geo.ritm.ru/restapi"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Content-Type": "application/json",
}
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

    async def _post_request(self, session: aiohttp.ClientSession, url, data) -> Any:
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

    async def fetch_objects_tree(self) -> GeoRitmObjectsTree:
        objects_data = {"sort": "name", "groupType": GROUP_TYPE}

        try:
            objects_tree_json = await self._post_request(
                self._session,
                f"{CORE_GEO_RITM_BASE_URL}/objects/objects-tree-set/",
                objects_data,
            )
            _LOGGER.info("Received data: %s", objects_tree_json)
            object_tree: GeoRitmObjectsTree = from_dict(
                data_class=GeoRitmObjectsTree, data=objects_tree_json[0]
            )

            return object_tree
        except ClientResponseError as e:
            if e.status == 401:
                await self.authenticate()
            raise e

    async def fetch_full_objects(self, objects_ids: list[int]) -> list[GeoRitmObject]:
        url = f"{CORE_GEO_RITM_BASE_URL}/objects/obj/"
        payload = {"objectId": objects_ids}

        objects_json = await self._post_request(self._session, url, payload)

        objects: GeoRitmObject = []
        for obj_json in objects_json:
            if int(obj_json["objType"]) == 1:
                obj_json["areas"] = await self.get_areas(obj_json["id"])
            objects += [from_dict(data_class=GeoRitmObject, data=obj_json)]

        return objects

    async def get_areas(self, deviceid):
        url = f"{CORE_GEO_RITM_BASE_URL}/objects/obj-areas/"
        payload = {"objectId": deviceid}

        areas_json = await self._post_request(self._session, url, payload)

        areas: ObjArea = []
        for area_json in areas_json:
            areas += [from_dict(data_class=ObjArea, data=area_json)]

        return areas

    async def _arm_disarm_object(self, area: int, imei: str, should_arm: bool) -> bool:
        action = "arm" if should_arm else "disarm"
        url = f"{CORE_GEO_RITM_BASE_URL}/objects/{action}/"
        payload = {"imei": imei, "area": area}

        try:
            result = await self._post_request(self._session, url, payload)
            _LOGGER.info("%s response is: %s", action, result)
            return result["success"] == 1
        except ClientResponseError as e:
            if e.status == 401:
                await self.authenticate()
            raise e

    async def arm_object(self, area: int, imei: str) -> bool:
        return await self._arm_disarm_object(area, imei, True)

    async def disarm_object(self, area: int, imei: str) -> bool:
        return await self._arm_disarm_object(area, imei, False)
