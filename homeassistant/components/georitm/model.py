from dataclasses import dataclass


@dataclass
class AreaZone:
    hasFault: bool
    num: int
    id: int
    hasAlarm: int
    name: str | None = None
    comment: str | None = None


@dataclass
class ObjArea:
    hasFault: int
    num: int
    id: int
    isGuarded: bool
    zones: list[AreaZone]
    hasAlarm: int
    name: str | None = None
    comment: str | None = None


@dataclass
class GeoRitmObjectState:
    hasFault: int
    isOnline: int
    isGuarded: int
    hasAlarm: int


@dataclass
class GeoRitmDevice:
    deviceType: int
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
    objectState: GeoRitmObjectState
    name: str
    addressShort: str
    id: int
    extId: int
    objType: int | str
    devices: list[GeoRitmDevice] | None = None
    objStatus: int | None = None
    isGsmOnline: bool | None = None
    canArm: bool | None = None
    isFromIDP: bool | None = None
    imei: str | None = None
    rev: str | None = None
    areas: list[ObjArea] | None = None


@dataclass
class GeoRitmObjectsTree:
    groupType: int
    objsGroups: list[str]
    name: str
    id: int
    objs: list[GeoRitmObject]
    nbItems: int
    extId: int | None = None
