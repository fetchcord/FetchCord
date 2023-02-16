#!/bin/bash

neofetch --stdout | grep "Shell" | awk -F: '{print $2}' | sed 's/^\s*//'
