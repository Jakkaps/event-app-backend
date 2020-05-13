FROM python:3.7


WORKDIR /flask_app

ADD .. /flask_app


RUN pip install .

CMD ["uwsgi", "event_app.ini"]
