import pandas as pd
# ------------------------------------------------------------------------------

LOOKUP_TABLE = 'csv_lookup_table.txt'

# ------------------------------------------------------------------------------

def setupPrefixes(file):
    prefixes = """@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .
    @prefix alchem: <https://glossa.uni-graz.at/context:alchem/ontology> .
    @prefix lat: <https://glossa.uni-graz.at/context:alchem/lat> .
    @prefix : <http://www.example.com/1/> .\n\n
    alchem:references a rdf:Property .\n\n
    """
    file.write(prefixes)

# ------------------------------------------------------------------------------

file = open("skos.txt", "w+") # open file in overwrite mode (so we don't add the prefixes 50 times)
setupPrefixes(file)

csv_lookup_table = pd.read_csv(LOOKUP_TABLE,
                     names=['lemma', 'concept','stem', 'regex', 'frequency'])

for index in csv_lookup_table.index:
    row = csv_lookup_table.loc[index]
    label = row["lemma"]
    concept = row["concept"]
    print("lat:" + label + " rdf:type skos:Concept;")
    print("  skos:prefLabel \"" + label + "\"@la;")
    print("  alchem:references alchem:" + concept + " .\n")
    file.write("lat:" + label + " rdf:type skos:Concept;\n")
    file.write("  skos:prefLabel \"" + label + "\"@la;\n")
    file.write("  alchem:references alchem:" + concept + " .\n\n")

file.close()

# ------------------------------------------------------------------------------
# FINIS
# ------------------------------------------------------------------------------
