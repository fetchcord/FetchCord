#!/bin/bash

neofetch --stdout | grep "Font" | awk -F: '{print $2}' | sed 's/^\s*//'
