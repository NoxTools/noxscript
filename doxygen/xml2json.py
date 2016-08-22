#!/usr/bin/env python
#
# Extracts all of the function names from the doxygen XML and generates a
# matching regex to be used for highlighting.
#
import json
import sys
import xml.etree.ElementTree as ET

def description_to_string(node):
    return '\n'.join([el.text or '' for el in node]).strip()

def main(path):
    tree = ET.parse(path)
    builtins = []
    for func in tree.findall(".//sectiondef[@kind='func']/memberdef[@kind='function']"):
        params = {}
        i = 0
        for param in func.findall('./param'):
            params[param.find('declname').text] = {
                'label': '%s %s' % (param.find('type').text, param.find('declname').text),
                'order': i,
            }
            i += 1
        for item in func.findall('.//parameteritem'):
            params[item.find('.//parametername').text]['documentation'] = description_to_string(item.find('.//parameterdescription'))
        builtins += [{
            'name': func.find('name').text,
            'text': '%s %s' % (func.find('definition').text, func.find('argsstring').text),
            'return': func.find('type').text,
            'brief': description_to_string(func.find('briefdescription')),
            'detailed': description_to_string(func.find('detaileddescription')),
            'signature': {
                'label': '%s %s' % (func.find('definition').text, func.find('argsstring').text),
                'documentation': description_to_string(func.find('briefdescription')),
                'parameters': list(sorted(params.values(), key=lambda x: x['order'])),
            },
        }]
    json.dump(builtins, sys.stdout)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s xml-file' % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1])
