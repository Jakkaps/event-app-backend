import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='shared_event',
    version='1.0',
    author='Oyvind Monsen',
    author_email='yvind.monsen@gmail.com',
    description='A data model of an event with datbase backing',
    long_description=long_description,
    url="",
    packages=setuptools.find_packages(),
    install_requires = [
        'elasticsearch',
        'mysql-connector-python',
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Licence :: OSI Approved :: MIT License",
        "Operating System :: Os Independent",
    ],
    python_requires='>=3.6',
    
)
