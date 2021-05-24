
import sys, re
import rdflib
from rdflib import Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, SKOS

ALCHEM = Namespace("https://glossa.uni-graz.at/context:alchem/")

# ------------------------------------------------------------------------------
def remove_namespace(string):
    alchem_namespace = "https://glossa.uni-graz.at/context:alchem/"
    if alchem_namespace in string:
        without_namespace = string.partition(alchem_namespace)[2]
        return without_namespace
    return string

# ------------------------------------------------------------------------------
def getConceptAsURI(string):
    namespace = 'https://glossa.uni-graz.at/context:alchem/'
    the_concept_with_ns = namespace + string
    uri = URIRef(the_concept_with_ns)

# ------------------------------------------------------------------------------
def uriIsInGraph(graph, uri):
    if ( ((uri, None, None) in graph) or ((None, None, uri) in graph) ):
        return True
    else:
        return False

# ------------------------------------------------------------------------------
def getContexts(graph, uri):
    uri_isA = []
    contexts = []
    for s, p, o in graph.triples((uri,  RDF.type, None)):
        uri_isA.append(o)
        print("{}\ta\t{}".format(remove_namespace(s), remove_namespace(o)))
    for type in uri_isA:
        for s, p, o in graph.triples((type,  ALCHEM.hasContext, None)):
            print("{}\thasContext\t{}".format(remove_namespace(s), remove_namespace(o)))
            contexts.append(str(o))
    #print("Current contexts for Uri:")
    #print(contexts)
    return contexts #TODO return list 
    # TODO creates error -
    # TODO Mercurius example abfangen

# ------------------------------------------------------------------------------

def normalizeSpace(xml):
    xml = re.sub(r'[>]', '> ', xml)
    xml = re.sub(r'[<]', ' <', xml)
    xml = re.sub(r'[.]', ' . ', xml)
    xml = re.sub(r'[,]', ' , ', xml)
    xml = re.sub(r'\s+', ' ', xml)
    return xml


# ------------------------------------------------------------------------------

def get_dictionary_key(dictionary, value):
    matching_keys = []
    for key, val in dictionary.items():
         if val == value:
             matching_keys.append(key)
    return matching_keys

# ------------------------------------------------------------------------------

def cleanupXMLUnicode(xml):
    #https://stackoverflow.com/questions/1707890/fast-way-to-filter-illegal-xml-unicode-chars-in-python
    _illegal_unichrs = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F),
                            (0x7F, 0x84), (0x86, 0x9F),
                            (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)]
    if sys.maxunicode >= 0x10000:  # not narrow build
            _illegal_unichrs.extend([(0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF),
                                     (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF),
                                     (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
                                     (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
                                     (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF),
                                     (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
                                     (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
                                     (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)])

    _illegal_ranges = ["%s-%s" % (chr(low), chr(high))
                       for (low, high) in _illegal_unichrs]
    _illegal_xml_chars_RE = re.compile(u'[%s]' % u''.join(_illegal_ranges))

    xml = _illegal_xml_chars_RE.sub(repl='',string=xml)
    return xml

# ------------------------------------------------------------------------------
def cleanOutShortItems(corpus_list):
    """
    Will normalize a corpus (given as list) by removing empty items and those of len < 3.
    """
    while "" in corpus_list:
        corpus_list.remove("")
    clean_list = [item for item in corpus_list if len(item) > 3]
    return clean_list
