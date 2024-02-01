FROM python:3.11

RUN apt-get update -y

WORKDIR /app

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN apt-get install -y default-mysql-client

