#! /usr/bin/env python3
# coding: utf-8

from os import sys
import subprocess, base64

with open(sys.argv[1], "r") as f:
    dump = base64.b64encode('\n'.join(f.readlines()).encode())

    try:
        subprocess.run(
            [
                "python",
                "-m",
                "fetch_cord",
                "-nfo",
                dump,
                "--nodistro"
            ],
            encoding="utf-8",
            stdout=sys.stdout,
            shell=False
        )
    except FileNotFoundError as err:
        print("Error: command invalid !")
        print(err)
    except subprocess.CalledProcessError as err:
        print("Error: Something happenned during execution ...")
        print(err)