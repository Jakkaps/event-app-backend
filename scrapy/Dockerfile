FROM selenium/standalone-chrome

WORKDIR /scrapy

Add . /scrapy

RUN sudo apt-get update
RUN sudo apt-get install python
RUN sudo apt-get install python3-pip -y
RUN pip3 install .

CMD ["python3", "EventCrawler/run_spiders.py"]
