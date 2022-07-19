import logging

from fastapi import APIRouter, Depends, Header, HTTPException, status
from ..models.pixoo_models import ChannelId, valid_point, valid_point_default
from ..models.request_models import TimerModel, DrawImageModel
from ..models.internal import Status
from pixo_rest.service.pixoo import Pixoo, get_pixoo_client, PixooSettings
from utils.config import get_config
from typing import Optional
import requests
from io import BytesIO


router = APIRouter()
_config = get_config()
logger = logging.getLogger(__name__)


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


@router.post('/screen/turn/{toggle}', tags=['main'], response_model=Status)
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


@router.post('/draw_image', tags=['draw'], response_model=Status)
async def draw_image(
    body: DrawImageModel,
    push: bool = False,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    """
    Отрисовка изображение на экране
    Можно сразу отправить на экран через атрибут push (в query string), или отложить до последующего вызова push()
    """
    try:
        img_content = requests.get(body.image_url).content
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Connection error'
        )
    except requests.exceptions.MissingSchema:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Not a valid URL'
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unknown error'
        )
    pixoo_client.draw_image(BytesIO(img_content))

    if push:
        pixoo_client.push()
        logger.info('Pushing image')

    return Status(status='ok')


@router.post('/draw_text', tags=['draw'], response_model=Status)
async def draw_text(
    text: str,
    x: Optional[int] = valid_point_default,
    y: Optional[int] = valid_point_default,
    push: bool = False,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    """
    Отрисовывает текст в позиции x, y
    Можно сразу отправить на экран через push (в query string), или отложить до последующего вызова push()
    """
    pixoo_client.draw_text(text=text, xy=(x, y))
    if push:
        pixoo_client.push()
        logger.info('Pushing text')
    return Status(status='ok')


@router.post('/push', tags=['draw'], response_model=Status)
async def push(
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    """
    Отправляет на экран изменения последних отрисовок
    """
    pixoo_client.push()
    return Status(status='ok')


@router.post('/draw_line', tags=['draw'], response_model=Status)
async def draw_line(
    x1: int = valid_point,
    y1: int = valid_point,
    x2: int = valid_point,
    y2: int = valid_point,
    push: bool = False,
    pixoo_client: Pixoo = Depends(get_pixoo_client),
    dependencies=Depends(verify_token),
):
    """
    Отрисовывает линию из позиции x1, y1 в позицию x2, y2
    Можно сразу отправить на экран через push (в query string), или отложить до последующего вызова push()
    """
    pixoo_client.draw_line(start_xy=(x1, y1), stop_xy=(x2, y2))
    if push:
        pixoo_client.push()
        logger.info('Pushing line')
    return Status(status='ok')
