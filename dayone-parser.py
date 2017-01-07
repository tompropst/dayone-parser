#!/usr/bin/python

# Copyright 2017 Thomas Propst
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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

# Check for only one separator option (XOR)
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
