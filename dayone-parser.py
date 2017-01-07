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
# -w    Week
#
# If a photo directory is provided, an image link will be inserted at the top
# of each entry. Specify the directory as:
# -p <dir>
#

import argparse
import os
import re
import string
# Use "from" here otherwise all references have to be "datetime.datetime"
from datetime import datetime
# However, then we need to explicitly import timedelta and others.
from datetime import timedelta
import urllib

parser = argparse.ArgumentParser(description = \
    "Convert a single, DayOne export file in markdown format to separate " +\
	"files.")
parser.add_argument("-v", help="Verbose output", action="store_true")
parser.add_argument("-i", help="Input file", required=True)
parser.add_argument("-o", help="Output directory", required=True)
parser.add_argument("-p", help="Photos directory", required=False)
parser.add_argument("-e", help="Separate by entry", action="store_true")
parser.add_argument("-d", help="Separate by day", action="store_true")
parser.add_argument("-w", help="Separate by week", action="store_true")
args = parser.parse_args()

# Check for only one separator option (XOR)
if not (args.e ^ args.d ^ args.w):
	print "A single separation option is required (-e, -d, -w)."
	exit(1)

if not os.path.isfile(args.i):
	print "No such file: " + args.i
	exit(2)

if not os.path.exists(args.o):
	try:
		os.makedirs(args.o)
	except:
		print "Unable to find or create output directory: " + args.o
		exit(3)

# Example date tags
#	Date:	December 6, 2010 at 9:00 AM
#	Date:	February 4, 2011 at 12:00 PM
#	Date:	February 28, 2011 at 10:48 AM
#	Date:	October 13, 2011 at 2:20 PM
dtMatch = r"\tDate:\t(January|February|March|April|May|June|July|August|September|October|November|December)\s[1|2|3]?\d,\s\d{4}\sat\s1?\d:\d\d\s[A|P]M"
ptMatch = r"\tPhoto:\t.+"
atMatch = r"\t[A-Z]\w+:\t.+"
dtFormat = r"%B %d, %Y at %I:%M %p"

def parseDate(dateLine):
	# As seen in dtMatch above, the date is the second tab delimited value.
	dateString = string.strip(string.split(dateLine, '\t')[2])
	dateObject = datetime.strptime(dateString, dtFormat)
	return dateObject

def checkGroup(dateTag):
	global currentGroup
	if not currentGroup: # This is the first group.
		currentGroup = dateTag
		return True
	if args.e: # Every date tag is a new group when separating by event.
		return True
	if args.d:
		if currentGroup.date() != dateTag.date():
			currentGroup = dateTag
			return True
	if args.w:
		# isocalendar returns (year, week, weekday)
		# It gracefully handles year end boundaries with 52 or 53 week years.
		# We only care about the year and week (and python indexing notation is
		# [start:lessthan] - that screws me up).
		currentIso = currentGroup.date().isocalendar()[0:2]
		dateTagIso = dateTag.date().isocalendar()[0:2]
		if currentIso != dateTagIso:
			currentGroup = dateTag
			return True
	return False

def startFile(dateTag):
	if args.e:
		fileName = dateTag.strftime("%Y-%m-%d_%H%M.markdown")
	if args.d:
		fileName = dateTag.strftime("%Y-%m-%d.markdown")
	if args.w:
		# I like my weekly journal files named by date of the first weekday.
		# The weekday is the 6th element of datetime.
		fileDate = dateTag - timedelta(days=dateTag.weekday())
		fileName = fileDate.strftime("%Y-%m-%d.markdown")
	filePath = os.path.join(args.o, fileName)
	try:
		fileHandle = open(filePath, "w+")
	except Exception, e:
		print "Unable to create file: " + filePath
		print e
		exit(3)
	return fileHandle

def parsePhoto(photoLine):
	photoFile = string.strip(string.split(photoLine, '\t')[2])
	if args.p:
		photoPath = os.path.join(args.p, photoFile)
		photoLink = "![photo]("+urllib.pathname2url(photoPath)+")"
	else:
		photoLink = photoLine
	return photoLink

currentFile = 0
currentGroup = 0

if args.v:
	print "Parsing file: " + args.i
	print "Writing new files to: " + args.o
with open(args.i) as inputFile:
	for line in inputFile:
		isDateTag = re.match(dtMatch, line)
		isPhotoTag = re.match(ptMatch, line)
		isAnyTag = re.match(atMatch, line)

		if isDateTag:
			dateTag = parseDate(line)
			isNewGroup = checkGroup(dateTag)
			if isNewGroup:
				if args.v:
					print "Starting new file."
				if currentFile:
					if not currentFile.closed:
						currentFile.close()
				currentFile = startFile(dateTag)
			currentFile.write("# " + string.strip(line)+'\n'+'\n')
			if args.v:
				print "Processing entry: " + string.strip(line)
		elif isPhotoTag and args.p:
			if args.v:
				print "Adding image link."
			photoLink = parsePhoto(line)
			currentFile.write(photoLink+'\n')
		elif isAnyTag: 
			currentFile.write("- "+line)
		else:
			currentFile.write('\n'+line)
