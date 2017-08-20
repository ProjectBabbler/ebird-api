#!/bin/sh

# Tests for the geo-observations script.

# Get observations near Cornell Laboratory of Ornithology
geo-observations --lat 42.48 --lng -71.45 --out -

# Missing values should be prompted for.
geo-observations --out -
