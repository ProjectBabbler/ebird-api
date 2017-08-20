#!/bin/sh

# Tests for the region-notable script.

# Get rare birds seen in Massachusetts.
region-notable --code US-MA --out -

# Missing required arguments are prompted for.
region-notable --out -
