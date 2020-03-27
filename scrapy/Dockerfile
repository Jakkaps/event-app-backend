FROM python:3.7

WORKDIR /scrapy

ADD . /scrapy

RUN pip install .

CMD ["python3", "EventCrawler/run_spiders.py"]
