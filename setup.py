# -*- coding:utf-8 -*-


import os
from setuptools import setup, find_packages


def read_file(file_name):
    return open(os.path.join(os.path.dirname(\
            __file__), file_name)).read().strip()


def get_install_requires():
    content = (read_file("requirements.txt")).strip("\n")
    return  tuple(content.split("\n"))


def get_version():
    return read_file('iclouder/VERSION')


setup(
    name="iclouder",
    version=get_version(),
    author="infinite.ft",
    author_email="infinite.ft@gmail.com",
    description="upload markdown document local \
            image and replace path automatically",
    long_description=read_file("README.rst"),
    url="https://github.com/free-free/mdimguploader",
    license="MIT",
    packages=find_packages(),
    install_requires=get_install_requires(),
    include_package_data=True,
    keywords=['markdown',],
    entry_points={
        'console_scripts': ['iclouder = iclouder.cmdline:execute']
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]    
)


