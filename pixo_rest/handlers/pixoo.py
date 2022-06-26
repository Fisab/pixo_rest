from fastapi import APIRouter, Depends
from ..models.pixoo_models import PixooTimer
from ..models.request_models import TimerModel
from ..models.internal import Status
from pixo_rest.service.pixoo import Pixoo, pixoo_client

router = APIRouter()


@router.post('/timer', tags=['main'], response_model=Status)
def set_timer(timer: TimerModel, pixoo_client: Pixoo = Depends(pixoo_client)):
    pixoo_client.set_timer(minute=timer.minute, second=timer.second)
    return Status('ok')
