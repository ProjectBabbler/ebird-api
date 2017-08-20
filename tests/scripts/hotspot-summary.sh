#!/bin/sh

# Tests for the hotspot-summary script.

# Get a list of species seen at Plum Island, Essex County, Massachusetts.
hotspot-summary --codes L830335 --out -

# Records for multiple hotspots can be fetched at once.
hotspot-summary --codes L830335 --codes L129046 --out -
