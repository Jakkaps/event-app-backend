from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-cors',
    'mysql-connector-python',
    'uwsgi',
    'selenium',
    'dateparser',
    'elasticsearch',
    'scrapy'
]

setup(
    name='event-app',
    version='1.0',
    description='The python backend for an app showing many events in Trondheim',
    author='Jens Kristoffersen',
    author_email='jensakrr@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
