from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall('__([a-z]+)__ = "([^"]+)"', fh.read()))
        return metadata["version"]


setup(
    name="Mopidy-Raspberry-GPIO",
    version=get_version("mopidy_raspberry_gpio/__init__.py"),
    url="https://github.com/pimoroni/mopidy-raspberry-gpio",
    license="Apache License, Version 2.0",
    author="Phil Howard",
    author_email="phil@pimoroni.com",
    description="Mopidy extension for GPIO input on a Raspberry Pi",
    long_description=open("README.rst").read(),
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    include_package_data=True,
    python_requires="> 2.7, < 3",
    install_requires=[
        "setuptools",
        "Mopidy >= 2.2",
        "Pykka >= 2.0",
    ],
    entry_points={
        "mopidy.ext": [
            "raspberry-gpio = mopidy_raspberry_gpio:Extension",
        ]
    },
    classifiers=[
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Multimedia :: Sound/Audio :: Players",
    ],
)
