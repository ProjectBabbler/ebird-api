#!/bin/sh

# Tests for the nearest-hotspots script.

# List the hotspots near Cornell Laboratory of Ornithology visited since yesterday
nearest-hotspots --lat 42.48 --lng -71.45 --back 1 --out -

# Missing required parameters are prompted for.
nearest-hotspots --out -
