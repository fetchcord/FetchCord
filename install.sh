#!/bin/bash

if [ $EUID -ne 0 ]; then
  echo "This script must to be run as root."
  exit 1
else
  cp fetchcord /usr/local/bin/
  chmod 755 /usr/local/bin/getde /usr/local/bin/getwm /usr/local/bin/fetchcord
  python3 setup.py install --root="/"
fi
