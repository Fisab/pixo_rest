from pydantic import BaseModel
from enum import Enum
from fastapi import Query


valid_point = Query(ge=0, le=64)
valid_point_default = Query(default=0, ge=0, le=64)


class ChannelId(str, Enum):
    face = 0  # часы
    cloud = 1  # подборка
    audio_visualizer = 2  # аудио-визуализатор (через микрофон)
    custom = 3  # сохраненки


class BasePixooModel(BaseModel):
    _Command: str


class PixooTimer(BasePixooModel):
    minute: int
    second: int
    status: int = 1


class PixooSettings(BaseModel):
    error_code: int
    Brightness: int
    RotationFlag: int
    ClockTime: int
    GalleryTime: int
    SingleGalleyTime: int
    PowerOnChannelId: int
    GalleryShowTimeFlag: int
    CurClockId: int
    Time24Flag: int
    TemperatureMode: int
    GyrateAngle: int
    MirrorFlag: int
    LightSwitch: int
