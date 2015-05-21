
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
#expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
#            "Trail", "Parkway", "Commons"]
expected  = ["name","type" ]
# UPDATE THIS VARIABLE
mapping = { #"St": "Street",
            #"St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "PALYA":"Palya",
            "Cir":"Circle",
            "BDA":"Bangalore Development Authority",
            "#" : ""
            }
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            return True
    return False

def is_street_name(elem):
    return (elem.attrib['k'] == "name") or (elem.attrib['k'] == "addr:housenumber")

def is_name_is_street(elem):
    """Some people fill the name of the street in k=name.
      Should change this"""
    s = street_type_re.search(elem.attrib['v'])
    #converting the upper case streets to lower
    return (elem.attrib['k'] == "name") and s and s.group().lower() in mapping.keys()

 
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
#     tree = ET.parse(osm_file, events=("start",))
    tree = ET.parse(osm_file)
    
    listtree = list(tree.iter())
    for elem in listtree:
        if elem.tag == "node" or elem.tag == "way":
            n_add = None
            
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    if audit_street_type(street_types, tag.attrib['v']):
                        #Update the tag attribtue
                        tag.attrib['v'] = update_name(tag.attrib['v'],mapping)
                elif is_name_is_street(tag):
                    tag.attrib['v'] = update_name(tag.attrib['v'],mapping)
                    n_add = tag.attrib['v']
                   
            if n_add:
                elem.append(ET.Element('tag',{'k':'addr:housenumber', 'v':n_add}))

            
                
    #write the to the file we've been audit
    tree.write(osmfile[:osmfile.find('.osm')]+'_audit.osm')
    return street_types

def update_name(name, mapping):
    """
    This is to prevent the shorter keys get first.
    """
    dict_map = sorted(mapping.keys(), key=len, reverse=True)
    for key in dict_map:
        
        if name.find(key) != -1:          
            name = name.replace(key,mapping[key])
            return name.lower()


    return  name.lower()

    


def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            #if name == "West Lexington St.":
            #    assert better_name == "West Lexington Street"
            #if name == "Baldwin Rd.":
             #   assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()
