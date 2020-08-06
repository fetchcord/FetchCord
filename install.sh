#!/bin/bash

if [ $EUID -ne 0 ]; then
  echo "This script needs to be run as root."
  exit
else
  cp fetch_cord/getdewm.sh /usr/local/bin/getdewm
  python3 setup.py install --root="/"
fi
