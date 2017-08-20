#!/bin/sh

# Tests for the region-observations script.

# Get all birds seen in Massachusetts.
region-observations --code US-MA --out -

# Missing required arguments are prompted for.
region-observations --out -

