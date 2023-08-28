#!/bin/bash

neofetch --stdout | grep "Kernel" | awk -F: '{print $2}' | sed 's/^\s*//'