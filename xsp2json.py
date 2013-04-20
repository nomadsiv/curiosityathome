# work in progress
# this parses xsp to json

#!/usr/bin/env python

from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="read GCode from file", metavar="FILE")
(options, args) = parser.parse_args()

def file_to_string():
    if options.filename:
        print "opening file " + str(options.filename)
        try:
            f = open(options.filename, 'r').read()
            return f[:f.index("~NAIF/SPC BEGIN COMMENTS~")]

        except Exception, e:
            print "file error " + str(e)
    else:
        print "Nothing to read. Please enter a filename with the -f option"


def main():
    print file_to_string()

main()
