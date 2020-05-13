FROM python:3.7

WORKDIR /scraper

ADD .. /scraper

RUN pip install .

CMD ["python3", "EventCrawler/run_spiders.py"]
