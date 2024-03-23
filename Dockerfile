FROM python:3.11.4

ENV PYTHONUNBUFFERED 1

RUN mkdir /task

COPY pricealertproject /task/pricealertproject

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /task/pricealertproject

RUN ls .
# VOLUME /tmp/pricealertproject

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && celery -A pricealertproject worker -l info
