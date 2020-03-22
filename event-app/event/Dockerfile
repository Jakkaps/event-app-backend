FROM python:3.7.2-stretch

WORKDIR /app

ADD . /app


RUN pip install .

CMD ["uwsgi", "run.py"]
