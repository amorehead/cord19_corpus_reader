################################################################################
#                                                                              #
#    CS 7740/8740                                                              #
#    Fall 2020 - Spring 2021                                                   #
#                                                                              #
#    Class Project - Generate Corpus Computations                              #
#    generate_corpus_computations.py                                           #
#                                                                              #
#    Started: Jason James                                                      #
#    2020-9-15                                                                 #
#                                                                              #
#    Modified: Alex Morehead                                                   #
#    2021-4-11                                                                 #
#                                                                              #
################################################################################

'''
The purpose of this script is to precompute the tokenized sentences from the
CORD-19 corpus. Basically, the script goes through each document parse file and
creates a corresponding file containing only the tokenized sentences from the
file. Tokenized sentences are stored as the text of a list of lists in the file:

file.write(str(sentences))

So, it should work to read the sentences back from the file with:

sentences = eval(file.read())

'''

import os

import nltk

from cord19 import CORD19CorpusReader

'''
Directory Hierarchy Diagram

munlp_f17/
    |-> f20/
        |-> code/
            |-> corpus_reader/
                |-> generate_corpus_computations.py

data/
    |-> archive/
        |-> document_parses/
            |-> pdf_json/
            |-> pmc_json/
    |-> tokenized_sentences
        |-> document_parses/
            |-> pdf_json/
            |-> pmc_json/


'''

# Specify where the corpus is actually stored at.
root = '../../../../data/archive/'

# Specify location to store computed data.
sentence_data = '../../../../data/tokenized_sentences/'
word_data = '../../../../data/tokenized_words/'
lemma_data = '../../../../data/lemmae/'
citation_data = '../../../../data/citations/'
metadata_data = '../../../../data/metadata/'

# Setup a corpus reader.
# include_titles = False and include_abstracts = False should omit titles and abstracts.
# prefer_pdf_parses = True and prefer_pmc_parses = True should grab all the JSON files.
reader = CORD19CorpusReader(root, '.*\.json', include_titles=False,
                            include_abstracts=False,
                            include_bodies=True,
                            prefer_pdf_parses=True,
                            prefer_pmc_parses=True)

# Print the number of files.
# Should be 123105 + 89432 = 212537.
# print(reader.fileids())
# print('len(reader.fileids():', len(reader.fileids()))

# Check if the directory for the tokenized sentences exists.
if (not os.path.exists(sentence_data)):
    # Create the directory.
    os.mkdir(sentence_data)

    # Create the subdirectories.
    os.mkdir(sentence_data + 'document_parses')
    os.mkdir(sentence_data + 'document_parses/pdf_json')
    os.mkdir(sentence_data + 'document_parses/pmc_json')

# Check if the directory for the tokenized words exists.
if (not os.path.exists(word_data)):
    # Create the directory.
    os.mkdir(word_data)

    # Create the subdirectories.
    os.mkdir(word_data + 'document_parses')
    os.mkdir(word_data + 'document_parses/pdf_json')
    os.mkdir(word_data + 'document_parses/pmc_json')

# Check if the directory for the lemmae exists.
if (not os.path.exists(lemma_data)):
    # Create the directory.
    os.mkdir(lemma_data)

    # Create the subdirectories.
    os.mkdir(lemma_data + 'document_parses')
    os.mkdir(lemma_data + 'document_parses/pdf_json')
    os.mkdir(lemma_data + 'document_parses/pmc_json')

# Check if the directory for the citations exists.
if (not os.path.exists(citation_data)):
    # Create the directory.
    os.mkdir(citation_data)

    # Create the subdirectories.
    os.mkdir(citation_data + 'document_parses')
    os.mkdir(citation_data + 'document_parses/pdf_json')
    os.mkdir(citation_data + 'document_parses/pmc_json')

# Check if the directory for the metadata exists.
if (not os.path.exists(metadata_data)):
    # Create the directory.
    os.mkdir(metadata_data)

    # Create the subdirectories.
    os.mkdir(metadata_data + 'document_parses')
    os.mkdir(metadata_data + 'document_parses/pdf_json')
    os.mkdir(metadata_data + 'document_parses/pmc_json')

# Grab the file IDs.
fileids = reader.fileids()

# Grab the nuber of iles.
file_count = len(fileids)

# Setup a Porter stemmer.
porter_stemmer = nltk.PorterStemmer()

# Grab the metadata for all the fileids.
metadata_dictionary = reader.metadata(fileids)

# Keep track of which file we're currently on.
current_file = 0

# Go through each file.
# for fileid in fileids[0:2]:
for fileid in fileids:

    # print('File ID:', fileid)

    # Display the current progress.
    if (current_file % 1000 == 0):
        print('File %d / %d' % (current_file, file_count))

    # Get the path for the file.
    (file_path, file_name) = os.path.split(fileid)
    # print('file_path', file_path)
    # print('file_name', file_name)

    # Get the file name without the file extension.
    file_name = os.path.splitext(os.path.basename(file_name))[0]
    # print('file_name', file_name)

    # Make a location for the new file.
    # sentence_file_location = sentence_data + file_path + '/' + file_name + '.txt'
    # word_file_location = word_data + file_path + '/' + file_name + '.txt'
    # lemma_file_location = lemma_data + file_path + '/' + file_name + '.txt'
    citation_file_location = citation_data + file_path + '/' + file_name + '.txt'
    metadata_file_location = metadata_data + file_path + '/' + file_name + '.txt'
    # print('word_file_location', word_file_location)

    # Grab the sentences for this document as a list.
    # sentences = list(reader.sents(fileid))
    # words = list(reader.words(fileid))
    # lemmae = list(sentences)
    citations = reader.citations(fileid)
    metadatas = metadata_dictionary[fileid]

    # # Go through all the sentences.
    # for i in range(0, len(sentences)):

    #     # Grab the sentence.
    #     sentence = sentences[i]

    #     # Stem the words in the sentence to get the lemmae.
    #     lemmae[i] = [porter_stemmer.stem(word) for word in sentence]

    # Open the file for these sentences.
    # sentence_file = open(sentence_file_location, 'w')
    # word_file = open(word_file_location, 'w')
    # lemma_file = open(lemma_file_location, 'w')
    citation_file = open(citation_file_location, 'w')
    metadata_file = open(metadata_file_location, 'w')

    # Write the list of sentences to the file.
    # sentence_file.write(str(sentences))
    # word_file.write(str(words))
    # lemma_file.write(str(lemmae))
    citation_file.write(str(citations))
    metadata_file.write(str(metadatas))

    # Close the file.
    # sentence_file.close()
    # word_file.close()
    # lemma_file.close()
    citation_file.close()
    metadata_file.close()

    # print(str(words))
    # print(str(lemmae))

    # print(str(sentences))
    # sentence_file = open(file_location, 'r')
    # sentences = sentence_file.read()
    # sentence_file.close()
    # print()
    # print()
    # print(str(sentences))

    # Update which file count we're on.
    current_file += 1
