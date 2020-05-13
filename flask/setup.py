from setuptools import setup, find_packages
import os 

requires = [
    'flask',
    'wheel',
    'flask-cors',
    'mysql-connector-python',
    'uwsgi',
    'shared_event'
]

setup(
    name='flask_event',
    version='0.0',
    description='A To-Do List built with Flask',
    author='Jens Kristoffersen',
    author_email='jensakrr@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    dependency_links=[
        "file:///Users/oyvind/Documents/programming/projects/web/event-app-backendevent/shared_event"
        # os.path.join(os.getcwd(), os.pardir, "event/dist/event-1.0-py3.7.egg")
    ]
)
