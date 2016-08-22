#!/usr/bin/env python
#
# Extracts all of the function names from the doxygen XML and generates a
# matching regex to be used for highlighting.
#
import sys
import xml.etree.ElementTree as ET

def main(path):
    tree = ET.parse(path)
    names = []
    for func in tree.findall(".//sectiondef[@kind='func']/memberdef[@kind='function']"):
        names += [func.find('name').text]
    print '(%s)' % '|'.join(names)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s xml-file' % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1])
