#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="rearr",
    version="0.2.0",
    description="Rearrange code inside Python modules",
    author="Michel Albert",
    author_email="michel@albert.lu",
    url="http://github.com/exhuma/rearr",
    license="MIT",
    install_requires=[
        "parso",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": {
            "rearr=rearr.rearr:main",
        }
    },
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
)
