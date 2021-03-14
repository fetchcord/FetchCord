#!/usr/bin/env python3
from os.path import dirname, join
import setuptools
import fetch_cord.__init__ as __init__

setuptools.setup(
    name="FetchCord",
    version=__init__.VERSION,
    description="grabs information about your Distro and displays it as Discord Rich Presence.",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MrPotatoBobx/FetchCord",
    author="MrPotatoBobx",
    author_email="junkahole23@protonmail.com",
    license="MIT",
    package_data={"fetch_cord": ["config_schema.json", "resources/default.conf", "resources/fetch_cord.conf", "resources/fetchcord_ids.json"]},
    packages=["fetch_cord"],
    include_package_data=True,
    install_requires=["pypresence", "psutil", "importlib-resources"],
    keywords=["distro", "info", "discord", "fetch"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "fetchcord=fetch_cord.__main__:main",
        ]
    },
)
