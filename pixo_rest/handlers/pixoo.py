from fastapi import APIRouter, Depends, Header, HTTPException, status
from ..models.pixoo_models import ChannelId
from ..models.request_models import TimerModel
from ..models.internal import Status
from pixo_rest.service.pixoo import Pixoo, get_pixoo_client, PixooSettings
from utils.config import get_config
from typing import Optional


router = APIRouter()
_config = get_config()


async def verify_token(x_token: str = Header()):
    if x_token != _config.app.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='go away')


@router.post('/timer', tags=['main'], response_model=Status)
def set_timer(
    timer: TimerModel,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    pixoo_client.set_timer(minute=timer.minute, second=timer.second)
    return Status(status='ok')


@router.post('/clock', tags=['main'], response_model=Status)
def set_clock(
    clock_id: Optional[int] = None,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    if clock_id is None:
        clock_id = pixoo_client.get_current_clock_id()
    pixoo_client.set_clock(clock_id=clock_id)
    return Status(status='ok')


@router.post('/brightness', tags=['main'], response_model=Status)
def set_brightness(
    brightness: int,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    pixoo_client.set_brightness(brightness=brightness)
    return Status(status='ok')


@router.post('/channel', tags=['main'], response_model=Status)
def set_channel(
    channel_id: Optional[ChannelId] = None,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    pixoo_client.set_channel(channel=channel_id)
    return Status(status='ok')


@router.post('/turn/{toggle}', tags=['main'], response_model=Status)
def turn(
    toggle: str,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    if toggle not in ['on', 'off']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='toggle must be on or off'
        )
    pixoo_client.turn_screen(on=toggle == 'on')
    return Status(status='ok')


@router.post('/turn/{toggle}', tags=['main'], response_model=Status)
def turn(
    toggle: str,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    if toggle not in ['on', 'off']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='toggle must be on or off'
        )
    pixoo_client.turn_screen(on=toggle == 'on')
    return Status(status='ok')


@router.get('/settings', tags=['main'], response_model=PixooSettings)
def turn(
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    return pixoo_client.get_settings()
