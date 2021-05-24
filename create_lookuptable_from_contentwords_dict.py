import sys
import os
cwd = os.getcwd()
dir_for_working_code = os.path.join(cwd, 'working-code')
sys.path.append(os.path.abspath(dir_for_working_code))
# ------------------------------------------------------------------------------

from annotation_list_creation_utilities import *
from kontroll_functionen import *
from csv_lookup_table import *
logger = ToDosLogger(LOG_FILE)

#CONTENT_WORD_FILE = 'content_words.txt'
CONTENT_WORD_FILE = 'concept_dict.txt'

# ------------------------------------------------------------------------------

corpus = readDirectoryAsCorpus("corpus")
#corpus = corpus[0:400000]

STOP_WORDS_LIST = getStopwords()


#bow_dict, reduced_corpus = updateBagOfWordsFromString(corpus, STOP_WORDS_LIST, content_words)
# ------------------------------------------------------------------------------

#displayBowDictEntries(content_words)

#freqDistHistogramForRemainingBowToDos(bow_dict)

orderContentWordDict(CONTENT_WORD_FILE)
content_words = readOneWordPerLineFileAsContentWordDict("content_words_ordered.txt")

createCSVLookupTableFromContentWordsDict(content_words, LOOKUP_TABLE)

csv_lookup_df = openCSVLookupTable(LOOKUP_TABLE)

print("\n---\n")
print(csv_lookup_df)
