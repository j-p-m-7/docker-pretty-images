#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="docker-pretty-images",
    version="1.0.0",
    description="Minimal pretty printer for `docker images`",
    author="j-p-m-7",
    url="https://github.com/j-p-m-7/docker-pretty-images",
    packages=find_packages(),
    scripts=["dockerprettyimages/bin/docker-pretty-images"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
