#!/bin/bash

neofetch --stdout | grep "Terminal" | awk -F: '{print $2}' | sed 's/^\s*//'
