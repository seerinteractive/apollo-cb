from setuptools import setup

with open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name = 'apollo-cb',
    version = '0.1',
    description = 'Make API requests with rate limiting',
    author = 'Ethan Lyon',
    author_email = 'ethanlyon@gmail.com',
    long_description = readme,
    install_requires = [
        'google-cloud-storage>=1.19.0',
        'google-api-python-client>=1.7.11'
        'aiohttp>=3.5.4',
        'async-timeout>=3.0.1',
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages = [
        'apollo', 
        'apollo.auth',
        'apollo.auth.apis', 
        'apollo.builder',
        'apollo.request',
        'apollo.storage',
        'apollo.utils',
    ]
)

__author__ = 'Ethan Lyon'