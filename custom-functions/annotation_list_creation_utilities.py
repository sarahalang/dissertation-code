
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from collections import Counter # for bow creation

import regex as re # sudo -H python3 -m pip install regex
from tqdm import tqdm # to display a progress bar

from nltk.probability import FreqDist

from ToDosLogger import *
from helper_functions import *
from cltk_based_text_processing import lemmatizeWord, getLemmaStrippedOfMarker, tokenizeLatinWords
from cltk.stem.latin.declension import CollatinusDecliner

# ------------------------------------------------------------------------------
def writeContentWordDictAsOneWordPerLineFile(content_words_dict, file_to_write_path):
    file = open(file_to_write_path, "w+") # open file in overwrite mode
    for key, value in content_words_dict.items():
        word_count = value[0]
        list_of_forms = " ".join(value[1])
        file.write(key + "," + str(word_count) +  "," + list_of_forms + "\n")
    file.close()

# ------------------------------------------------------------------------------
def readOneWordPerLineFileAsContentWordDict(file_path):
    content_words_dict = {}
    with open(file_path,  'r+') as f: #TODO opens in read mode, better a+?
        lines = f.read().splitlines()
        for line in lines:
            items = line.split(",")
            key = items[0]
            word_count = int(items[1])
            regex_list = items[2].split(" ")
            content_words_dict[key] = [word_count, regex_list]
        return content_words_dict

# ------------------------------------------------------------------------------
def orderContentWordDict(file_path):
    """
    Will read a content word dict .txt file and write it back to the same place but ordered.

    It will read it from a file and write it back to the file
    """
    content_words_dict = readOneWordPerLineFileAsContentWordDict(file_path)
    ordered_dict = {}
    ordered_as_list = sorted(content_words_dict.keys(), key=lambda x:x.lower())
    print(ordered_as_list)
    for item in ordered_as_list:
        ordered_dict[item] = content_words_dict[item]
    file_name = file_path.split(".")
    safe_file_path_to_write_to = file_name[0] + "_ordered.txt"
    writeContentWordDictAsOneWordPerLineFile(ordered_dict, safe_file_path_to_write_to)
    return ordered_dict

# ------------------------------------------------------------------------------
def informAboutCurrentProgress(bow_dict, corpus):
    original_corpus_length_unique = getCorpusSize(corpus)
    current_bow_size = len(bow_dict)
    frequency_distribution = FreqDist(corpus.split())
    frequency_distribution.plot(40,title='Frequency distribution for 40 most common tokens')
    print("\nCorpus has [" + str(original_corpus_length_unique) + \
      "] unique values, of which [" + str(current_bow_size) + "] are still in the BOW to be processed.")
    showProgressBar(original_corpus_length_unique, current_bow_size)

# ------------------------------------------------------------------------------
def getContentWordsDict():
    """
    A function to load content words from a txt file.
    """
    content_words = readOneWordPerLineFileAsContentWordDict("content_words.txt")
    # should create the file if it doesn't exist
    return content_words

# ------------------------------------------------------------------------------
def createNewEntryInContentWordDict(word, count_value, content_words_dict):
    normalized_word_forms = prepareForStopwordList(word)
    normalized_word_forms.append(word) # add the exact word form which was found
    # which might not be normalized - so remains accessible for annotation later
    word_set = set(normalized_word_forms)
    forms_to_add = list(word_set)
    count = count_value # of dict
    lemma = lemmatizeWord(normalizeWord(word))
    content_words_dict[lemma] = [count, forms_to_add]
    return content_words_dict, forms_to_add

# ------------------------------------------------------------------------------
def addToContentWordEntry(word_form, count_value, content_words_dict):
    key = lemmatizeWord(normalizeWord(word_form)) # list with one item
    key_count = count_value
    if key in content_words_dict:
        new_count = key_count + int(content_words_dict[key][0])
        content_words_dict[key][1].append(word_form)
        new_regexes = content_words_dict[key][1]
        content_words_dict[key] = [new_count, new_regexes]
    return content_words_dict

# ------------------------------------------------------------------------------
def batchUpdateContentWordEntryWordCount(forms_added, bow_dict, content_words_dict):
    total_count = 0
    for word_form in forms_added:
        if word_form in bow_dict:
            count = bow_dict[word_form]
            total_count += count
            bow_dict.pop(word_form)
    key = lemmatizeWord(normalizeWord(word_form)) # list with one item
    if key in content_words_dict:
        regexes = content_words_dict[key][1]
        content_words_dict[key] = [total_count, regexes]
    return content_words_dict, bow_dict


# ------------------------------------------------------------------------------
def removeProcessedContentWordsFromBOW(tokens, content_words):
    bow_dict_types_list = [value[1] for key, value in content_words.items()]
    bow_types = []
    for types_list in bow_dict_types_list:
        bow_types += types_list
    bow_types = normalizeList(bow_types)

    corpus_tokens = tqdm(tokens)
    corpus_tokens.set_description("Removal of already processed content words")
    tokens_without_normalized_content_words = [w for w in corpus_tokens if not normalizeWord(w) in bow_types]


    corp_toks = tqdm(tokens_without_normalized_content_words)
    corp_toks.set_description("Removal of already processed content words (normalized)")
    tokens_without_content_words = [w for w in corp_toks if not w in bow_types]
    print("After: " + str(len(tokens_without_content_words)))
    return tokens_without_content_words

# ------------------------------------------------------------------------------
def addItemToContentWordDictIfNotAlreadyIn(original_word, count_value, content_words, bow_dict):
    finding = [key for key, value in content_words.items() if original_word in value[1]]
    found_normalized = [key for key, value in content_words.items() if normalizeWord(original_word) in value[1]]
    if finding:
        print("was found - nothing to be done")
        bow_dict.pop(original_word)
    elif found_normalized:
        current_key = found_normalized[0] # only checks the first one - even when there are more finds!
        print("Found in normalized form! Adding original form..")
        content_words = addToContentWordEntry(original_word, count_value, content_words)
        bow_dict.pop(original_word)
    else:
        print("Word wasn't yet in the dict, adding now...")
        content_words, forms_added = createNewEntryInContentWordDict(original_word, \
                                     count_value, content_words)
        content_words, bow_dict = batchUpdateContentWordEntryWordCount(forms_added, bow_dict, content_words)
    return content_words, bow_dict


# ------------------------------------------------------------------------------
def quitBOWProcessing(bow_dict, STOP_WORDS_LIST, content_words):
    print("\n---\nWriting this new stopword list to file.")
    updateStopwordList(STOP_WORDS_LIST)
    print("Writing the current state of content words to file.")
    writeContentWordDictAsOneWordPerLineFile(content_words, "content_words.txt")
    print("\n---\nBye for now!")

# ------------------------------------------------------------------------------
def printMostFrequentContentWords(content_words):
    print("\n---\nThose are the lemmata in the content word list so far:")
    sorted_bow = sorted(content_words.items(), key=lambda key: key[0][0])
    for item in sorted_bow:
        print(item)

# ------------------------------------------------------------------------------
def bowProcessingInfo():
    print("\n\n\n----------------")
    print("You will now be prompted to add items to the content words list.")
    print("Say [s/n/-] for STOPS or [k/y/+/ENTER] for KEEP.\n[q] to quit.")
    print("If you keyboard-interrupt, all data will be lost.\n So please be sure to actually quit.")

# ------------------------------------------------------------------------------
def processOneBOWItem(corpus, bow_dict, content_words, STOP_WORDS_LIST):
    sorted_bow = sorted(bow_dict, key=bow_dict.get, reverse=True)
    key = sorted_bow[0]
    value = bow_dict[key]
    while True:
        answer = input("[ " + key + " | " + str(value) + " ] ") #  to stops? [y/n] -- [q to quit]
        if (answer == 'n') or (answer == 's') or (answer == '-'):
            new_forms = prepareForStopwordList(key)
            new_forms.append(key)
            while("" in new_forms):
                new_forms.remove("")
            STOP_WORDS_LIST = STOP_WORDS_LIST + new_forms
            bow_dict.pop(key)
            break
        elif (answer == 'y') or (answer == '') or (answer == 'k') or (answer == 'c') or (answer == '+'):
            # pass value to adding function
            content_words, bow_dict = addItemToContentWordDictIfNotAlreadyIn(key, value, content_words, bow_dict)
            break
        elif answer == 'q':
            informAboutCurrentProgress(bow_dict, corpus)
            quitBOWProcessing(bow_dict, STOP_WORDS_LIST, content_words)
            quit()
        else:
            continue
    return bow_dict, content_words, STOP_WORDS_LIST


# ------------------------------------------------------------------------------
def updateStopwordList(new_stopwords):
    """
    This will simply write the current stopwords list to the respective file.
    It will, however, also overwrite the contents of the old file,
    if applicable.
    """
    stop_set = set(new_stopwords)
    new_stopwords_unique = list(stop_set)
    writeListAsOneWordPerLineFile(new_stopwords_unique, "stop_word_list.txt")

# ------------------------------------------------------------------------------
def addToStopWords(STOP_WORDS_LIST, list_of_new_words, logger):
    new_stops = STOP_WORDS_LIST
    declined_forms = (list_of_new_words, "adding declined stopwords", logger)
    new_stops += declined_forms
    updateStopwordList(new_stops)
    # TODO error happens with list of lists..

# ------------------------------------------------------------------------------
def prepareForStopwordList(word):
    logger = ToDosLogger(LOG_FILE)
    lemma = getLemmaStrippedOfMarker(lemmatizeWord(normalizeWord(word)))
    decliner = CollatinusDecliner()
    results = []
    try:
        declined_forms = decliner.decline(lemma, flatten=True)
        unique_values = set(declined_forms)
        results = list(unique_values)
    except:
        logger.addToLogger("STOPS", "WARNING", "Lemma couldn't be declined: " + word)
        results.append(word)
    return results


# ------------------------------------------------------------------------------
def updateBagOfWordsFromString(corpus, STOP_WORDS_LIST, content_words):
    """
    Creates a bag of words from a corpus (as string). Using CLTK for Latin.

    Will remove linebreak-hyphens and punctuation as well as stopwords.
    WILL NOT lowercase (!) - so truecasing can be done later, if needed.
    """
    print("\n---\nUpdating the bag of words...")
    normalized = removeHyphensAndPunctuation(corpus)
    #tokens = normalized.split() # this would be the non-Latin/language specific way
    tokens = tokenizeLatinWords(normalized)
    corpus_without_stopwords = removeStopwordsFromTokens(STOP_WORDS_LIST, tokens)
    corpus_without_already_processed_content_words = removeProcessedContentWordsFromBOW(corpus_without_stopwords, content_words)
    reduced_corpus = corpus_without_already_processed_content_words
    reduced_corpus = cleanCorpus(reduced_corpus)
    bow_dict = Counter(corpus_without_already_processed_content_words)

    # remove all items where count is 1 (TODO ggf change later)
    dict_items = tqdm(bow_dict.items())
    dict_items.set_description("Removing hapaxes")
    bow_dict_without_hapaxes = {key:val for key, val in dict_items if val != 1}
    # also remove all keys that are just one letter
    bow_dict_without_one_letters = {key:val for key, val in bow_dict_without_hapaxes.items() if len(key) != 1}
    print("After removing 1-letter words and hapaxes: " + str(len(bow_dict_without_one_letters)) + " left.")
    return bow_dict_without_one_letters, reduced_corpus

# ------------------------------------------------------------------------------
# ggf delete TODO
def updateBagOfWordsFromDictFile(corpus, STOP_WORDS_LIST, content_words):
    """
    Creates a bag of words from a corpus (as string). Using CLTK for Latin.

    Will remove linebreak-hyphens and punctuation as well as stopwords.
    WILL NOT lowercase (!) - so truecasing can be done later, if needed.
    """
    print("\n---\nUpdating the bag of words...")
    corpus_without_stopwords = removeStopwordsFromTokens(STOP_WORDS_LIST, corpus)
    corpus_without_already_processed_content_words = removeProcessedContentWordsFromBOW(corpus_without_stopwords, content_words)
    reduced_corpus = corpus_without_already_processed_content_words
    reduced_corpus = cleanCorpus(reduced_corpus)
    bow_dict = Counter(corpus_without_already_processed_content_words)

    bow_dict_without_hapaxes = {key:val for key, val in bow_dict.items() if val != 1}
    print("After removing 1-letter words and hapaxes: " + str(len(bow_dict_without_hapaxes)) + " left.")
    return bow_dict_without_hapaxes, reduced_corpus

# ------------------------------------------------------------------------------
def updateBagOfWordsFromList(corpus_list, STOP_WORDS_LIST, content_words):
    """
    Creates a bag of words from a corpus (as string). Using CLTK for Latin.

    Will remove linebreak-hyphens and punctuation as well as stopwords.
    WILL NOT lowercase (!) - so truecasing can be done later, if needed.
    """
    print("\n---\nUpdating the bag of words...")

    corpus_without_stopwords = removeStopwordsFromTokens(STOP_WORDS_LIST, corpus_list)
    corpus_without_already_processed_content_words = removeProcessedContentWordsFromBOW(corpus_without_stopwords, content_words)
    reduced_corpus = corpus_without_already_processed_content_words
    reduced_corpus = cleanCorpus(corpus_without_already_processed_content_words)
    bow_dict = Counter(reduced_corpus)

    return bow_dict, reduced_corpus

# ------------------------------------------------------------------------------
# FINIS
# ------------------------------------------------------------------------------
