#!/bin/bash
pyver=$(python3 --version | grep -o "3..")
if [ ! $pyver ]; then
  echo "Python3 must be installed to use this script, exiting."
  exit 1
fi
if [ $EUID -ne 0 ]; then
  echo "This script must be run as root."
  exit 1
else
  dir="/usr/local/bin/"
  python3 setup.py install --root="/"
  ln -sf /lib/python$pyver/site-packages/fetch_cord/run-rpc.py /usr/local/bin/fetchcord
  chmod 755 ${dir}fetchcord
  exit 0
fi
