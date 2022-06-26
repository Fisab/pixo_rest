from pydantic import BaseModel


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
