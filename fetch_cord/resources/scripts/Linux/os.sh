#!/bin/bash

neofetch --stdout | grep "OS" | awk -F: '{print $2}' | sed 's/^\s*//'
