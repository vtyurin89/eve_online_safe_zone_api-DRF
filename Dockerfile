FROM python:3.11

RUN apt-get update -y

WORKDIR /app

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

#CMD ["python", "manage.py", "migrate", "0.0.0.0:8000"]