import sys
import os
cwd = os.getcwd()
dir_for_working_code = os.path.join(cwd, 'custom-functions')
sys.path.append(os.path.abspath(dir_for_working_code))
# ------------------------------------------------------------------------------

from ToDosLogger import *
#from annotation_list_creation_utilities import getContentWordsDict, updateBagOfWordsFromString
#from helper_functions import *
from cltk_based_text_processing import stemLemma, getLemmaStrippedOfMarker

# ------------------------------------------------------------------------------

import numpy as np
# ------------------------------------------------------------------------------

LOOKUP_TABLE = 'csv_lookup_table.txt'
CONTENT_WORDS_DICT = 'content_words_dict.txt'

# ------------------------------------------------------------------------------
def displayBowDictEntries(content_words_dict):
    print("There are currently " + str(len(content_words_dict)) + " entries in your Content Words.")
    sorted_bow = sorted(content_words_dict, key=content_words_dict.get, reverse=True)
    new_bow = {}
    for i in sorted_bow:
        the_bow_item = content_words_dict[i]
        count = the_bow_item[0]
        forms_list = the_bow_item[1]
        key = i
        new_bow[key] = count
        #print(key + ", " + str(count))
    sorted_bow = sorted(new_bow, key=new_bow.get, reverse=True)
    for i in sorted_bow:
        print(i, new_bow[i])

# ------------------------------------------------------------------------------
def openCSVLookupTable(file_name):
    """
    Reads .txt file as the CSV Lookup Table.
    Returns Pandas DataFrame.
    """
    csv_lookup_table = pd.read_csv(file_name,
                         names=['lemma', 'concept','stem', 'regex', 'frequency'])
    csv_lookup_table.frequency = csv_lookup_table.frequency.astype(int)
    return csv_lookup_table

# ------------------------------------------------------------------------------

def createCSVLookupTableFromContentWordsDict(content_words_dict, file_name):
    """
    Creates a CSV Lookup Table from a Content Words dictionary.

    The dictionary has the lemma as the key and contains a list,
    where list[0] contains the frequency count and
    list[1] contains a list of word forms.

    The resulting lookup table contains the lemma
    but also creates a preliminary concept from this lemma,
    a stem for this lemma,
    a "regex", i.e. the list of word forms found in the corpus for later annotation,
    and also the word frequency.

    Creates a txt file which can be read as CSV.
    """
    file = open(file_name, "w+") # overwrite mode!
    for key, value in content_words_dict.items():
        lemma = getLemmaStrippedOfMarker(key)
        frequency_count = value[0]
        unique_word_form_values = list(set(value[1]))
        word_forms = " ".join(value[1]) # make string
        preliminary_concept = getLemmaStrippedOfMarker(key)
        stem = stemLemma(lemma)
        file.write(lemma + "," + preliminary_concept + "," + stem + "," + \
                   word_forms + "," + str(frequency_count) + "\n")
        file.flush()
    file.close()

# ------------------------------------------------------------------------------


#cell.sort_values("warnInfoError")

#existing_error_types = self.logs_list["ErrorType"].unique().tolist()

#lookup_table = pd.DataFrame(columns=['lemma', 'concept','stem', 'regex', 'frequency'])




# ------------------------------------------------------------------------------
# FINIS
# ------------------------------------------------------------------------------
