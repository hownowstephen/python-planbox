import os, shutil
from setuptools import setup, find_packages

setup(
    name = "python-planbox",
    version = "0.0.1",
    author = "Stephen Young",
    author_email = "stephen@tryllo.com",
    description = ("Python interface to the planbox API"),
    url = "https://github.com/stephenyoung/python-planbox",
    packages= ['planbox'],
    package_data={'': ['planbox.yaml']},
    install_requires=[
        'pyyaml>=3.09',
    ]
)