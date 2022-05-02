FROM python:3

ENV PYTHONUNBUFFERED = 1

# RUN mkdir /scapp
WORKDIR /scapp

# ADD . /scapp

# COPY requirements.txt ./
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


