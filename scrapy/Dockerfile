FROM python:3.7

WORKDIR /scrapy

Add . /scrapy

RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y


RUN pip install .

COPY ./cron_file /etc/cron.d/cron_file

CMD ["cron", "-f"]
