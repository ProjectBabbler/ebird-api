#!/bin/sh

# Tests for the hotspot-observations script.

# Get observations from Plum Island, Essex County, Massachusetts.
hotspot-observations --codes L830335 --out -

# Records for multiple hotspots can be fetched at once.
hotspot-observations --codes L830335 --codes L129046 --out -
