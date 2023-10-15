# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
WORKDIR /code/funproxy
#RUN apt-get update -y && apt-get upgrade -y && apt-get install -y --no-install-recommends binutils libproj-dev gdal-bin libgdal-dev python3-gdal
