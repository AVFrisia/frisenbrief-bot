FROM python:3

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y pandoc build-essential libxml2-dev libxslt1-dev antiword unrtf poppler-utils tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig texlive-extra-utils

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./FrisenbriefBot.py" ]
