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
  if [ -d /usr/lib/python3*/ ]; then
  ln -sf /usr/lib/python3*/*-packages/fetch_cord/run-rpc.py /usr/local/bin/fetchcord
  elif [ -d /lib/python3*/ ]; then
  ln -sf /lib/python3*/*-packages/fetch_cord/run-rpc.py /usr/local/bin/fetchcord
  elif [ -d /usr/loca/lib/python3*/ ]; then
  ln -sf /usr/lib/python3*/*-packages/fetch_cord/run-rpc.py /usr/local/bin/fetchcord
  else
    echo "Unknown python path, cannot symlink, contact me on github to resolve this."
  fi

  chmod 755 ${dir}fetchcord
  exit 0
fi
