#!/usr/bin/env python
from setuptools import setup
import sys
import os

setup(
    name = "capbreak",
    version = "0.1",
    author='zhxgigi',
    author_email='zhxgigi@gmail.com',
    packages  = [
        "capbreak"
    ],
    package_dir = {
        "capbreak" : "solutions"
    },
    package_data = {
        "capbreak" : [
            os.path.join('models', 'zonehorg', "*.model"),
            os.path.join('models', 'zonehcn', "*.model")
        ]
    }
)