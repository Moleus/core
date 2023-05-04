"""Constants for the georitm-client integration."""

from dataclasses import dataclass
import logging

from homeassistant.const import Platform

DOMAIN = "georitm"
LOGGER = logging.getLogger(__package__)


CONF_HOST = "host"
CONF_LOGIN = "login"
CONF_PASSWORD = "password"

PLATFORMS = [Platform.BINARY_SENSOR]


@dataclass
class GeoRitmObjectState:
    hasFault: int
    isOnline: int
    isGuarded: int
    hasAlarm: int


@dataclass
class GeoRitmDevice:
    deviceType: int
    shell: str
    name: str
    description: str
    imei: str
    shortName: str
    firmware: str
    apiURLbase: str
    shellSwf: str
    picture: str


@dataclass
class GeoRitmObject:
    rev: str
    objectState: GeoRitmObjectState
    isFromIDP: bool
    devices: list[GeoRitmDevice]
    isGsmOnline: bool
    objStatus: int
    canArm: bool
    name: str
    imei: str
    addressShort: str
    id: int
    extId: int
    objType: str


@dataclass
class GeoRitmObjecsTree:
    groupType: int
    objsGroups: list[str]
    name: str
    id: int
    objs: list[GeoRitmObject]
    nbItems: int
    extId: int | None = None
