import sys
import os
cwd = os.getcwd()
dir_for_working_code = os.path.join(cwd, 'custom-functions')
sys.path.append(os.path.abspath(dir_for_working_code))

# ------------------------------------------------------------------------------

from csv_lookup_table import openCSVLookupTable
from helper_functions import writeListAsOneWordPerLineFile

# ------------------------------------------------------------------------------

LOOKUP_TABLE = 'csv_lookup_table.txt'
OUTPUT_FILE = 'turtle.txt'
TODO_FILE = 'kos_TODO.txt'

# ------------------------------------------------------------------------------
switchcase = {
    'a' : ':animal',
    'm' : ':mythologicalFigure',
    't' : ' TODO '
    } # this is an example, add more as you please

# ------------------------------------------------------------------------------
def promptUserWithInfo(switchcase):
    print("Input single letter corresponding to the desired output.\n")
    print("x \t move on to next entry \t\t t \t to add TODO and a TODO message")
    print("q \t quit, left to do will be saved to " + TODO_FILE)
    for letter, concept in switchcase.items():
        print(letter + " \t " + concept)

# ------------------------------------------------------------------------------
def getUserInputForThesaurus(file, list_item, switchcase):
    """
    Function to prompt user to generate a KOS from a list and given options.
    User can quit but
    """
    first = True
    running = True
    while(running):
        letter = input("---\nWaiting for input..\n")
        if letter.isalpha():
            letter = letter.lower()
        if letter == 'x':
            if not first:
                print(" .\n\n")
                file.write(" .\n\n")
                file.flush()
            break
        elif letter == 'q':
            if not first:
                print(" .\n\n")
                file.write(" .\n\n")
                file.flush()
            running = False
            return running
        elif letter not in switchcase:
            print("Please input a letter which is mapped (see list above.)")
            print("To get to the next entry, use 'x'!")
            print("To get to the next entry, use 'q'!")
            continue
        else:
            triple = switchcase.get(letter)
            if first:
                print("alchem:" + list_item + " a ")
                file.write("alchem:" + list_item + " a ")

            if letter == 't': # t means TODO and asks for a message
                print("\n" + triple)
                file.write("\n" + triple)
                message = input("Please enter a TODO message, finish with ENTER:")
                print(message + "\n")
                file.write(message + "\n")
            else:
                if first:
                    first = False
                    print(triple)
                    file.write(triple)
                else:
                    print(" , " + triple)
                    file.write(" , " + triple)
    return running

# ------------------------------------------------------------------------------
# RUN PROGRAM
# ------------------------------------------------------------------------------

csv_lookup_df = openCSVLookupTable(LOOKUP_TABLE)
concepts_list = csv_lookup_df['concept'].tolist()
print(concepts_list)

# ------------------------------------------------------------------------------

file = open(OUTPUT_FILE, "a+") # open file in append mode
running = True

while concepts_list and running: # empty list is implicity boolean in python
    for entry in concepts_list:
        promptUserWithInfo(switchcase)
        print("[ " + entry + " ]\n")
        running = getUserInputForThesaurus(file, entry, switchcase)
        if not running:
            writeListAsOneWordPerLineFile(concepts_list, TODO_FILE)
            print("Progam ended after saving progress to file.")
            break
        concepts_list.remove(entry)

file.close()

# ------------------------------------------------------------------------------
# FINIS
# ------------------------------------------------------------------------------
