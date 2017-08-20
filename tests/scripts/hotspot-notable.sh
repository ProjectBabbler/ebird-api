#!/bin/sh

# Tests for the hotspot-notable script.

# Get rare birds seen at Plum Island, Essex County, Massachusetts.
hotspot-notable --codes L830335 --out -

# Records for multiple hotspots can be fetched at once.
hotspot-notable --codes L830335 --codes L129046 --out -
