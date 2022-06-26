from pydantic import BaseModel
from pixo_rest.models.pixoo_models import PixooTimer


class TimerModel(PixooTimer):
    __exclude_fields__ = ['Status', 'Command']
