from pydantic import BaseModel


class PixooSettings(BaseModel):
    ip: str


class Config(BaseModel):
    pixoo: PixooSettings
