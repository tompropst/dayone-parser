# DayOne Journal Parser

The [DayOne journal app](http://dayoneapp.com/) for iOS and OSX allows you to export journal entries but all entries are exported into a single file. I wrote this Python script to parse that file (in markdown format) into separate files for each entry, day, or week.

## Usage

Once you [export your entries](http://help.dayoneapp.com/exporting-entries/) in markdown format, you will have a single markdown file and optionally, a photos directory. Run the `dayone-parser.py` script with a separator option and path to your exported markdown file to produce separate files.

For separate files by entry, use:

````
$ ./dayone-parser.py -e <filename>
````

