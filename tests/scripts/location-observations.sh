#!/bin/sh

# Tests for the location-observations script.

# Get observations from Plum Island, Essex County, Massachusetts.
location-observations --codes L830335 --out -

# Records for multiple locations can be fetched at once.
location-observations --codes L830335 --codes L129046 --out -
