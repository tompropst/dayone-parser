#!/usr/bin/python

# DayOne Journal Parser
# Convert a single markdown file into separate files for each entry, day(, 
# week).
# Specify the period with one of the following options:
# -e    Entry
# -d    Day
# -w    Week (not yet implemented)
#
# If a photo directory is provided, an image link will be inserted at the top
# of each entry. Specify the directory as:
# -p <dir>
#

import argparse

parser = argparse.ArgumentParser(description = \
    "Convert a single, DayOne export file in markdown format to separate " +\
	"files.")
parser.add_argument("inputFile")
parser.add_argument("-v", "--verbose", help="Verbose output", 
    action="store_true")
parser.add_argument("-e", help="Separate by entry", action="store_true");
parser.add_argument("-d", help="Separate by day", action="store_true");
parser.add_argument("-w", help="Separate by week", action="store_true");
args = parser.parse_args()

if not (args.e ^ args.d ^ args.w):
	print "A single separation option is required (-e, -d, -w)."
	exit(1)

