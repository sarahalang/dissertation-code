import sys
import os
cwd = os.getcwd()
dir_for_working_code = os.path.join(cwd, 'custom-functions')
sys.path.append(os.path.abspath(dir_for_working_code))
# ------------------------------------------------------------------------------

from ToDosLogger import *
from helper_functions import normalizeList
from cltk_based_text_processing import stemLemma, getLemmaStrippedOfMarker
from csv_lookup_table import *
from xml_and_rdf_functions import *

# ------------------------------------------------------------------------------

import numpy as np
import re
import uuid
import unicodedata
# ------------------------------------------------------------------------------

LOOKUP_TABLE = 'csv_lookup_table.txt'
XML = 'viatorium_full.xml'
ANNOTATED_XML = 'viatorium_annotated.xml'

# ------------------------------------------------------------------------------

xml = ''
with open(XML, "r", encoding="utf8") as fh_in:
    xml = fh_in.read()

xml = normalizeSpace(xml)
# ------------------------------------------------------------------------------

broken_up_words_dict = {}

lb_regex = re.compile('(\w+)([¬-]\s?<lb/>\s?)(\w+)')

tuple_of_broken_up_words = re.findall(lb_regex, xml)
for item in tuple_of_broken_up_words:
    tup_as_list = list(item)
    find = ''.join(tup_as_list)
    without_lb = tup_as_list[0] + tup_as_list[2]
    broken_up_words_dict[find] = without_lb

list_of_broken_up_words_in_xml = list(broken_up_words_dict.values())

# ------------------------------------------------------------------------------

lookup_table_df = openCSVLookupTable(LOOKUP_TABLE)

for index in lookup_table_df.index:
    row = lookup_table_df.loc[index]
    label = row["lemma"]
    concept = row["concept"]
    regex = row["regex"]
    regex_list = regex.split(" ")
    extra_regexes = [] # empty list is false
    is_broken_up =  any(item in regex_list for item in list_of_broken_up_words_in_xml)
    if is_broken_up:
        list_intersection = list(set(regex_list) & set(list_of_broken_up_words_in_xml))
        new_regexes = []
        for item in list_intersection:
            form_to_add = get_dictionary_key(broken_up_words_dict, item)
            new_regexes += form_to_add
        extra_regexes += new_regexes

    all_regexes = regex_list + extra_regexes
    all_regexes.sort(key=lambda s: len(s))
    all_regexes.reverse()
    all_regexes = cleanOutShortItems(all_regexes)
    if not all_regexes: # falls nach dem Aussortieren kurzer Einträge nichts mehr drin ist
        continue

    regex_string = " | ".join(all_regexes)
    regex_for_annotation = "( " + regex_string + " )"
    regex_search = re.compile(regex_for_annotation)

    xml = re.sub(pattern=regex_search, repl=f' <term ana=\"{concept}\" xml:id=\"{concept + "-" + str(uuid.uuid4())[-8:-1]}\">\g<1></term> \n', string=xml)

    xml = normalizeSpace(xml)
    xml = cleanupXMLUnicode(xml)
    with open(ANNOTATED_XML, 'w+', encoding="utf-8") as xml_output:
        xml_output.write(xml)
    print("\n---\nLast item processed: " + concept + "\n")

# ------------------------------------------------------------------------------

# re-normalize punctuation
xml = re.sub(r' [,]', ',', xml)
xml = re.sub(r' [.]', '.', xml)

# repair document declaration, otherwise XML parsers will be offended
xml = re.sub(r'(\s<\?xml version="1\. 0")', '<?xml version=\"1.0\"', xml)
# add some linebreaks or Oxygen XML will suffer an OutOfMemory Error
xml = re.sub(r'(</teiHeader>|<pb n|  <TEI>)', '\n\g<1>', xml)
# remove <p> elements via regex since they don't make sense and will disturb
# the following step
xml = re.sub(r'(</p>|<p>)', '\n', xml)

# ------------------------------------------------------------------------------

with open(ANNOTATED_XML, 'w+', encoding="utf-8") as xml_output:
    xml_output.write(xml)

print("The Dataframe used had " + str(lookup_table_df.size / 5) + " entries.")

# ------------------------------------------------------------------------------
# FINIS
# ------------------------------------------------------------------------------
