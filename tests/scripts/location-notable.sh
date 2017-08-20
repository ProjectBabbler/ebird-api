#!/bin/sh

# Tests for the location-notable script.

# Get rare birds seen at Plum Island, Essex County, Massachusetts.
location-notable --codes L830335 --out -

# Records for multiple locations can be fetched at once.
location-notable --codes L830335 --codes L129046 --out -
