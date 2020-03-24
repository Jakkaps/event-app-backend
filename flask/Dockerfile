FROM python:3.7


WORKDIR /app

ADD . /app


RUN pip install .

CMD ["uwsgi", "event_app.ini"]
