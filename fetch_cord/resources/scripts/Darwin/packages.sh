#!/bin/bash

neofetch --stdout | grep "Packages" | awk -F: '{print $2}' | sed 's/^\s*//'
