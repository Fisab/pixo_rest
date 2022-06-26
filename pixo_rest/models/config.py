from pydantic import BaseModel


class PixooSettings(BaseModel):
    ip: str


class AppSettings(BaseModel):
    token: str
    root_path: str


class Config(BaseModel):
    pixoo: PixooSettings
    app: AppSettings
