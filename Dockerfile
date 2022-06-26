FROM arm32v7/python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

COPY pixo_rest ./pixo_rest
COPY utils ./utils

RUN python3 -m pip install --upgrade pip
RUN sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev
RUN python3 -m pip install -r requirements.txt


CMD ["uvicorn", "pixo_rest.__main__:app", "--host", "0.0.0.0", "--port", "80"]