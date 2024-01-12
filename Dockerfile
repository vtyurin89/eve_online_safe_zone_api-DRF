FROM python:3.11

RUN apt-get update -y

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]