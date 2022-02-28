FROM python:3

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y pandoc antiword build-essential

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./FrisenbriefBot.py" ]
