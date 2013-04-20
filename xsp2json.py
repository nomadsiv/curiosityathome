#!/usr/bin/env python

# work in progress
# this parses xsp to json


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
            return f

        except Exception, e:
            print "file error " + str(e)
    else:
        print "Nothing to read. Please enter a filename with the -f option"


def cleanup(f):
    return f[:f.index("~NAIF/SPC BEGIN COMMENTS~")]


def main():
    file_content = file_to_string()
    print cleanup(file_content)


main()
