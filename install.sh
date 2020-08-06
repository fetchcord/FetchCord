#!/bin/bash

if [ $EUID -ne 0 ]; then
  echo "This script needs to be run as root."
  exit
else
  cp fetch_cord/*.sh  /usr/local/bin/getdewm
  chmod 755 /usr/local/bin/getde /usr/local/bin/getwm
  python3 setup.py install --root="/"
fi
