#!/bin/sh

# Tests for the list-species script.

# Get all the species in the eBird database.
list-species --out -

# Get all the spuhs (usually species which are very similar).
list-species --category spuh --out -
