#!/bin/sh

# Tests for the list-hotspots script.

# List hotspots visited in Nevada in the past 10 days.
list-hotspots --code US-NV --back 10 --out -

# Missing values are prompted for.
list-hotspots --out -
