from setuptools import setup, find_packages

requires = [
    'scrapy',
    'mysql-connector-python',
    'selenium',
    'dateparser'
]

setup(
    name='scrapy_events',
    version='0.0',
    description='Spiders for crawling the web for events',
    author='Jens Kristoffersen',
    author_email='jensakrr@gmail.com',
    keywords='scrapy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
