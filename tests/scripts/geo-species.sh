#!/bin/sh

# Tests for the geo-species script.

# Get observations of Red-naped Sapsucket near Cornell Laboratory of Ornithology.
geo-species --species 'Sphyrapicus nuchalis' --lat 42.48 --lng -71.45 --out -

# Missing values should be prompted for.
geo-species --out -
