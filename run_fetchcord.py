#!/usr/bin/env python3
"""Standalone launcher used by the PyInstaller build (fetchcord.spec).

Runs the real package entry point so relative imports inside the package
resolve correctly when bundled into a single-file binary.
"""

from fetch_cord.__main__ import main

if __name__ == "__main__":
    main()
