#!/bin/sh

# Tests for the region-species script.

# Get records of Red-naped Sapsucker from Essex County, Massachusetts.
region-species --species 'Sphyrapicus nuchalis' --code US-MA-009 --out -

# Missing required arguments are prompted for.
region-species --out -
