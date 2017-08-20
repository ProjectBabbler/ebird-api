#!/bin/sh

# Tests for the geo-notable script.

# Get the list of rare birds seen near Cornell Laboratory of Ornithology.
geo-notable --lat 42.48 --lng -71.45 --out -

# Missing values should be prompted for.
geo-notable --out -
