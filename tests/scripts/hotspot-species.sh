#!/bin/sh

# Tests for the hotspot-species script.

# Get records of Red-naped Sapsucker from Plum Island, Essex County, Massachusetts.
hotspot-species --species 'Sphyrapicus nuchalis' --codes L830335 --out -

# If species is missing the name is prompted for.
hotspot-species --codes L830335 --out -
