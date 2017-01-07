# DayOne Journal Parser

The [DayOne journal app](http://dayoneapp.com/) for iOS and OSX allows you to export journal entries but all entries are exported into a single file. I wrote this Python script to parse that file (in markdown format) into separate files for each entry, day, or week.

## Usage

Once you [export your entries](http://help.dayoneapp.com/exporting-entries/) in markdown format, you will have a single markdown file and optionally, a photos directory. Run the `dayone-parser.py` script with a separator option and path to your exported markdown file to produce separate files.

For separate files by entry, use:

````
$ ./dayone-parser.py -e -i <filename> -o <output path>
````

If you prefer to have only one file per day or week, use the respective option in place of `-e`. You must specify one option.

If you want photo tags converted to markdown image links, add the `-p` option. This option requires the path to the location where the images will be. This is not necessarily where they currently are but rather where the link in the resulting markdown will point. You may want to provide a URL or relative path depending on where you will put the photos.

## Requirements

The following modules are used. All of these should be included in a standard Python installation.

- argparse
- os
- re
- string
- datetime
- urllib

