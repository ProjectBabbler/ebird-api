#!/bin/sh

# Tests for the location-species script.

# Get records of Red-naped Sapsucker from Plum Island, Essex County, Massachusetts.
location-species --species 'Sphyrapicus nuchalis' --code L830335 --out -

# If species is missing the name is prompted for.
location-species --codes L830335 --out -
