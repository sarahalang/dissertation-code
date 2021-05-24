# dissertation-code
Repository mit dem Code zur Dissertation.



# Documentation 

All the `.py` files in this repository should be run in a command line environment and take no parameters. 
The names of the files they manipulate are hard-coded as constants in the code and need to be modified there, if needed. 
They are set to run correctly on the examples files in this repo, in the directory order as it is here. 

# Order of Usage 
The scripts in this repository are meant to work together as one workflow. 
It is explained in the text of the dissertation which - at the time being - is not yet available to the public.
It is very possible that this workflow might not make sense to you without the explanations provided in the dissertation text. 

While it can certainly make sense to use single ones of these scripts outside of this workflow, 
it will be necessary to provide suitable data to start with, of course. 

The example files provided here will work with the scripts as they are and they should be operated in the following order.
Most of these scripts will simply run through, displaying a few log messages. Others will require the user to make decisions and provide inputs, notably  `KOS-generator.py`, `create_SKOS.py` and `create_list_of_content_words.py`.


1) We begin with `create_list_of_content_words.py` which will read in the whole corpus (located in a folder `corpus` as `.txt` files) and the system will prompt us to sort words into stop words and content words.
Unlike in many out-of-the-box uses of Natural Language Processing, we don't want to use stop words to clean our corpus but rather, the remaining items in our content words list are like a to do list.
We want to classify each word either as a stopword (as in: not relevant for our purposes, even though it might not be a stopword in the common sense of a finite list of typical stopwords but rather a domain-specific stopword list
where stopword is the opposite of content word, i.e. a word relevant to our domain). The words the command line tool presents us with to sort through have already been stripped of a standard list of stopwords and 
will be presented to us sorted by frequency of appearance. What is presented to us are types, not lemmata. Once we add them to either the list of stopwords or the list of content words, the algorithm will try to lemmatize them and clean the corpus of their lemmata. This system is somewhat complicated but it allows us to save non-standard glyphs (like long s, etc.) along with other lemmata, so they too will be found later in the annotation stage without us having to normalize the TEI transcriptions of historical texts in which those glyphs have been preserved. 
This process will update our stopword and content word lists, so we can stop and resume the process whenever necessary. 
In the case here, the tool was used to step down from the most frequent terms through to types which appear only between 15-30 times. 
This already yielded about 1000 entries saved in our content word list - at which point the selection process for words to be annotated was stopped. 
Now these words need to be reviewed manually as there are quite many mistakes in the lemmatization (as described in the dissertation chapter on the technical implementation of the method). 
After cleaning them out, removing superfluous ones or ones which were deemed not that useful for the annotation, 680 entries were left.  
2) Having reviewed and manually cleaned out the content words dictionary (as CSV), it needs to be read in again using `create_lookuptable_from_contentwords_dict.py` which will create the actual lookup table (CSV too).  
At the same time, both `KOS-generator.py` and  `create_SKOS.py` can be run.  `create_SKOS.py` will simple create SKOS data for the concepts, whereas `KOS-generator.py` expects the user to step through the list of concepts and to determine how to classify them for the Knowledge Organization System. The user can select from a choice of pre-configured properties to speed up the KOS creation process or can add their own relations or mark things with `TODO` to come back to them later. 
3) Now you need to make sure you have an example (more or less) TEI/XML file ready (like the example `viatorium_full.xml` which results from Transkribus machine transcription using the NOSCEMUS GM4 model (outputted as XML/TEI). 
This XML data has then been cleaned according to the description in the dissertation text. Mostly, it contains `<lb/>`, `<pb/>`, `<note>`, `<p>` and `<head>` elements. 
The `TEIheader` hasn't been filled out properly (so there isn't much of a chance of accidentally annotating unwanted things in the header) and the `<facsimile>` element has been modified slightly for later ingest into the 
GAMS content management system and removed to another file for the time being. It will be added again later (after all steps mentioned here have been completed, together with a proper `TEIheader`) for ingest into the GAMS.  
4) `annotate_xml.py` will annotate the terms from the CSV lookup table on a given XML file (constant `XML`) and save its output to the file name specified in the constant `ANNOTATED_XML`. Further constants are `LOOKUP_TABLE` and `CONTENT_WORDS_DICT`.
5) The next step is to use the `decknamen-kwic-generator.xsl` on `test-kwic.xml` which will give `kwic-test-result.xml`.
6) Then, `process_KWIC_XML.py` is used to generate results of the context analysis from the helper XML containing the KWICs. It will write results to the KWIC's `<result>` child element. The context counts will be stored in the attributes of `<context>` elements.


# XSL Transformation settings
In some parts of the workflow, XSL transformations are used. 
In order to test them, you need to combine them as follows.


`decknamen-kwic-generator.xsl` used on `test-kwic.xml` will give `kwic-test-result.xml`. 

`visualize-KWIC-as-HTML.xsl` is to be used on `KWIC_RDF_result.xml` and will produce`kwic-test-result.html`. 



 
