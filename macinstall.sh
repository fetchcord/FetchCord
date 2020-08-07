#!/bin/bash
if [ $EUID -ne 0 ]; then
  echo "This script must be run as root."
  exit 1
else
  python3 setup.py install --root="/"
