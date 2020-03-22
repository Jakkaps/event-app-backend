from setuptools import setup, find_packages

requires = [
    'scrapy',
    'scrapyd',
    'mysql-connector-python'
]

setup(
    name='scrapy_events',
    version='0.0',
    description='Spiders for crawling the web for events',
    author='Jens Kristoffersen',
    author_email='jensakrr@gmail.com',
    keywords='scrapy',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = EventCrawler.settings']},
    include_package_data=True,
    install_requires=requires
)
