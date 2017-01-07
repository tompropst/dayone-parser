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
import os
import re
import string

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

if not os.path.isfile(args.inputFile):
	print "No such file: " + args.inputFile
	exit(2)

# Example date tags
#	Date:	December 6, 2010 at 9:00 AM
#	Date:	February 4, 2011 at 12:00 PM
#	Date:	February 28, 2011 at 10:48 AM
#	Date:	October 13, 2011 at 2:20 PM
dtMatch = r"\tDate:\t(January|February|March|April|May|June|July|August|September|October|November|December)\s[1|2|3]?\d,\s\d{4}\sat\s1?\d:\d\d\s[A|P]M"

with open(args.inputFile) as inputFile:
	for line in inputFile:
		isDateTag = re.match(dtMatch, line)
		if isDateTag:
			print string.strip(line)
