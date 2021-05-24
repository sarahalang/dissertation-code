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

import xml.etree.ElementTree as ET

import rdflib
from rdflib import Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, SKOS

from collections import Counter

# ------------------------------------------------------------------------------

LOOKUP_TABLE = 'csv_lookup_table.txt'
XML = 'kwic-test-result.xml'
RESULT_XML = 'KWIC_RDF_result.xml'
KOS = "kos-example.ttl"

# ------------------------------------------------------------------------------

ALCHEM = Namespace("https://glossa.uni-graz.at/context:alchem/")
graph = rdflib.Graph()
graph.parse(KOS, format="n3")
graph.bind('alchem', URIRef('https://glossa.uni-graz.at/context:alchem/'))

# ------------------------------------------------------------------------------

tree = ET.parse(XML)
root = tree.getroot()
kwics = root.findall('KWIC')

# ------------------------------------------------------------------------------

for kwic in kwics:
    kwics_terms = []
    xml_id = ''
    if 'n' in kwic.attrib:
        pass
    if '{http://www.w3.org/XML/1998/namespace}id' in kwic.attrib:
        xml_id = kwic.attrib['{http://www.w3.org/XML/1998/namespace}id']
        #print(kwic.attrib['{http://www.w3.org/XML/1998/namespace}id']) # result ID

    terms = kwic.findall('TEXT/term')
    for term in terms:
        if 'ana' in kwic.attrib:
            concept = term.attrib['ana']
            kwics_terms.append(concept)
    #print("Kwics terms:")
    #print(kwics_terms)
    print()
    total_contexts = []
    not_found_list = []
    for concept in kwics_terms:
        contexts_list = []
        uri = getConceptAsURI(concept)
        if uriIsInGraph(graph, uri):
            contexts = getContexts(graph, uri)
            contexts_list += contexts
        else:
            not_found_list.append(concept)
        total_contexts += contexts_list

    concept_counter = Counter(total_contexts)
    print(concept_counter)
    for node in kwic.findall('result'):
        termsInKWIC=ET.Element('termsInKWIC')
        termsInKWIC.text = " ".join(kwics_terms)
        node.append(termsInKWIC)
        for key, value in concept_counter.items():
            new_result_entry=ET.Element('context')
            new_result_entry.attrib['name'] = remove_namespace(key)
            new_result_entry.attrib['n'] = str(value)
            node.append(new_result_entry)
    for node in kwic.findall('log'):
        node.attrib['xml:space'] = 'preserve'
        node.text = " ".join(kwics_terms)

# ------------------------------------------------------------------------------

xml_str = ET.tostring(root, encoding='unicode')
xml = cleanupXMLUnicode(xml_str)

result_file = open(RESULT_XML, "w+")
result_file.write(xml)

# ------------------------------------------------------------------------------
# FINIS
# ------------------------------------------------------------------------------
