from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-cors',
    'mysql-connector-python',
    'uwsgi'
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
    install_requires=requires
)
