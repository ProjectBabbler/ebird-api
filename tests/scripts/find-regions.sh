#!/bin/sh

# Tests for the find-regions script.

# Find subnational1 areas with 'west' in their name.
find-regions --rtype subnational1 --match west --out -

# Missing values should be prompted for.
find-regions --out -
