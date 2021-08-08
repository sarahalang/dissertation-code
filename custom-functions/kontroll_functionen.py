import sys
import os
cwd = os.getcwd()
dir_for_working_code = os.path.join(cwd, 'working-code')
sys.path.append(os.path.abspath(dir_for_working_code))

from ToDosLogger import *

#from annotation_list_creation_utilities import getContentWordsDict, updateBagOfWordsFromString
#from helper_functions import *
#from cltk_based_text_processing import createNERListFromCorpus

# ------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------

def freqDistHistogramForRemainingBowToDos(bow_dict):
    sorted_bow = sorted(bow_dict, key=bow_dict.get, reverse=True)
    most_frequent_item = sorted_bow[0]
    highest_frequency_count = bow_dict[most_frequent_item]
    step = 5
    max_steps = int(highest_frequency_count / step)
    print("Max steps: " + str(max_steps) + ". Highest freq in corpus: " + str(highest_frequency_count))
    frequencies = [0] * (max_steps+1)
    one_to_five = [0] * 6
    one_to_five.append(0)
    for lemma, count in bow_dict.items():
        frequency_range = int(count / 5)
        #print("Frequency range for lemma [" + lemma + "], count: " + str(count) + ", freq: " + str(frequency_range))
        frequencies[frequency_range] += 1
        if not frequency_range: # i.e. its smaller than 5
            one_to_five[count] += 1
    print(frequencies)
    print("---")
    print(one_to_five)
    plotFrequencyList_LargeNumbers(frequencies)
    plotFrequencyList_OneToFive(one_to_five)

# ------------------------------------------------------------------------------
def plotFrequencyList(freq_list):
    plt.hist(freq_list, density=True)  # density=False would make counts; , bins=30
    plt.ylabel('Frequency (5er)')
    plt.xlabel('Type count');
    plt.show()

# ------------------------------------------------------------------------------
def plotFrequencyList_OneToFive(frequencies):
    heights = [int(freq/5) for freq in frequencies]
    heights_normalized = [(h*5) for h in heights]
    plt.bar(heights_normalized, height=heights_normalized)
    plt.yticks(heights_normalized, heights_normalized)
    plt.xticks(heights_normalized, ['0','1','2', '3', '4', '5'])
    plt.ylabel('Frequency (5er Sprünge)')
    plt.xlabel('Type count between 1-5');
    plt.show()

# ------------------------------------------------------------------------------
def plotFrequencyList_LargeNumbers(freq_list):
    labels = [i for i in range(len(freq_list))]
    fiver = [(l*5) for l in labels]
    #print("Labels:")
    #print(labels)
    heights = [int(freq/5) for freq in freq_list]
    heights_normalized = [(h*5) for h in heights]
    plt.bar(heights_normalized, height=heights_normalized)
    #plt.hist(heights_normalized)  # density=False would make counts; , bins=30, , density=True
    plt.yticks(heights_normalized, heights_normalized)
    plt.xticks(heights_normalized, fiver)
    plt.ylabel('Frequency (5er)')
    plt.xlabel('Type count');
    plt.show()
    #plt.bar(x, height=)
    #plt.xticks(x, ['a','b','c'])

# ------------------------------------------------------------------------------
# FINIS
# ------------------------------------------------------------------------------
