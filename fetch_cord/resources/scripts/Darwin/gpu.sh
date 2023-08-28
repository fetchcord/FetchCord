#!/bin/bash

lspci -mmQ | grep 3D | cut -d " " -f1 --complement | sed -e 's/" "/\t/g' -e 's/\"//g' | cut -f1 --complement --output-delimiter=" "