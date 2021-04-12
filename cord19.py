################################################################################
#                                                                              #
#    CS 7740/8740                                                              #
#    Fall 2020 - Spring 2021                                                   #
#                                                                              #
#    Class Project - CORD-19 Corpus Reader                                     #
#    cord19.py                                                                 #
#                                                                              #
#    Started: Jason James                                                      #
#    2020-9-15                                                                 #
#                                                                              #
#    Modified: Alex Morehead & Jian Liu                                        #
#    2021-4-12                                                                 #
#                                                                              #
################################################################################

"""
A reader for the CORD-19 corpus.
"""

import csv
import json
import nltk.data
import os
from nltk.corpus.reader.api import *
from nltk.corpus.reader.util import *
from nltk.tokenize import *


class CORD19CorpusReader(CorpusReader):
    """
    Reader for the CORD19 corpus:
    https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge .

    Documents in the CORD-19 corpus are stored as JSON in text files, so the
    implementation of this reader is based on the implementation of the 
    PlaintextCorpusReader in NLTK.
    """

    CorpusView = StreamBackedCorpusView

    def __init__(
            self,
            root,
            # Don't allow files to be explicitly specified anymore.
            # TODO: Make it where it's alright for a list of files?
            fileids,
            word_tokenizer=WordPunctTokenizer(),
            sent_tokenizer=nltk.data.LazyLoader("tokenizers/punkt/english.pickle"),
            para_block_reader=read_blankline_block,
            encoding="utf8",
            include_titles=True,
            include_abstracts=True,
            include_bodies=True,
            # TODO: What to include for the bibliographies?
            # include_bibliographies = True,
            prefer_pdf_parses=True,
            prefer_pmc_parses=False
    ):
        # TODO: Gather up the list of fileids to pass into the constructor.

        CorpusReader.__init__(self, root, fileids, encoding)

        # print('self.fileids:', self._fileids)

        self._word_tokenizer = word_tokenizer
        self._sent_tokenizer = sent_tokenizer
        self._para_block_reader = para_block_reader

        self._include_titles = include_titles
        self._include_abstracts = include_abstracts
        self._include_bodies = include_bodies
        # self._include_bibliographies = include_bibliographies

        # Save location of the metadata.csv file.
        self._metadata_file = root + 'metadata.csv'

        # Record encoding scheme
        self._encoding = encoding

        # Check if don't want both PDF parses and PMC parses.
        if (not (prefer_pdf_parses and prefer_pmc_parses)):

            # Make an empty dictionary to hold the metadata.
            metadata_dictionary = defaultdict(list)

            # Open the CSV file.
            csv_file = open(self._metadata_file, 'r', newline='', encoding=self._encoding)

            # Try finding the dialect.
            dialect = csv.Sniffer().sniff(csv_file.read())

            # Reset to the beginning of the file.
            csv_file.seek(0)

            # Setup a CSV reader on the file.
            csv_reader = csv.DictReader(csv_file, dialect=dialect)

            # Go through each row in the metadata.
            for row in csv_reader:
                # Use the cord_uid as the key and append the row.
                # The entries are lists sense a cord_uid can appear in multiple rows.
                metadata_dictionary[row['cord_uid']].append(row)

            # for (key, value) in metadata_dictionary.items():
            #     if (len(value) > 1):
            #         print(key, 'has > 1 list')

            # print(metadata_dictionary['soow2ehe'])

            # TODO: Probably faster to construct a new list of files rather than remove unwanted ones?
            # Make an empty list to hold the new fileids list.
            new_fileids_list = []

            # Go through all the entries in metadata.
            for (entry_key, entry_value) in metadata_dictionary.items():

                # TODO: Collpase this with the handling for list size of one?
                # Check if there's multiple items in this entry.
                if (len(entry_value) > 1):

                    has_pdf_parse = False
                    has_pmc_parse = False
                    pdf_parse_value = ''
                    pmc_parse_value = ''

                    # Gotta go through the entries in here.
                    for entry in entry_value:

                        # Check if there's a PDF parse.
                        if (entry['pdf_json_files'] != ''):
                            # Set that there is.
                            has_pdf_parse = True

                            # Store off the value.
                            pdf_parse_value = entry['pdf_json_files']

                        # Check if there's a PMC parse.
                        if (entry['pmc_json_files'] != ''):
                            # Set that there is.
                            has_pmc_parse = True

                            # Store off the value.
                            pmc_parse_value = entry['pmc_json_files']

                    # Check if there was neither a PDF parse nor a PMC parse.
                    if (not has_pdf_parse and not has_pmc_parse):

                        # Just go to the next one.
                        continue

                    # Check if there's PDF parses, but not PMC parses.
                    elif (has_pdf_parse and not has_pmc_parse):

                        # The PDF parses can actually be a list of files.
                        # So, get the list of PDF parse files.
                        pdf_parses_file_list = pdf_parse_value.split('; ')

                        # Go through each file.
                        for pdf_parse_file in pdf_parses_file_list:
                            # Append this file to the new list.
                            new_fileids_list.append(pdf_parse_file)

                    # Check if there's PMC parses, but not PDF parses.
                    elif (has_pmc_parse and not has_pdf_parse):

                        # Append this file to the new list.
                        new_fileids_list.append(pmc_parse_value)

                    # There must be both PDF parses and PMC parses.
                    else:

                        # Check if prefer PDF parses.
                        if (prefer_pdf_parses):

                            # The PDF parses can actually be a list of files.
                            # So, get the list of PDF parse files.
                            pdf_parses_file_list = pdf_parse_value.split('; ')

                            # Go through each file.
                            for pdf_parse_file in pdf_parses_file_list:
                                # Append this file to the new list.
                                new_fileids_list.append(pdf_parse_file)

                        # Check if prefer PMC parses.
                        elif (prefer_pmc_parses):

                            # Append this file to the new list.
                            new_fileids_list.append(pmc_parse_value)

                # Otherwise, only one entry.
                else:

                    # Grab the entry, which is the first thing on the list.
                    entry = entry_value[0]

                    # Check if there was neither a PDF parse nor a PMC parse.
                    if (entry['pdf_json_files'] == '' and entry['pmc_json_files'] == ''):

                        # Just go to the next one.
                        continue

                    # Check if there's PDF parses, but not PMC parses.
                    elif (entry['pdf_json_files'] != '' and entry['pmc_json_files'] == ''):

                        # The PDF parses can actually be a list of files.
                        # So, get the list of PDF parse files.
                        pdf_parses_file_list = entry['pdf_json_files'].split('; ')

                        # Go through each file.
                        for pdf_parse_file in pdf_parses_file_list:
                            # Append this file to the new list.
                            new_fileids_list.append(pdf_parse_file)

                    # Check if there's PMC parses, but not PDF parses.
                    elif (entry['pmc_json_files'] != '' and entry['pdf_json_files'] == ''):

                        # Append this file to the new list.
                        new_fileids_list.append(entry['pmc_json_files'])

                    # There must be both PDF parses and PMC parses.
                    else:

                        # Check if prefer PDF parses.
                        if (prefer_pdf_parses):

                            # The PDF parses can actually be a list of files.
                            # So, get the list of PDF parse files.
                            pdf_parses_file_list = entry['pdf_json_files'].split('; ')

                            # Go through each file.
                            for pdf_parse_file in pdf_parses_file_list:
                                # Append this file to the new list.
                                new_fileids_list.append(pdf_parse_file)

                        # Check if prefer PMC parses.
                        elif (prefer_pmc_parses):

                            # Append this file to the new list.
                            new_fileids_list.append(entry['pmc_json_files'])

            # print('len(new_fileids_list):', len(new_fileids_list))
            # print('new_fileids_list:', new_fileids_list)
            # print('len(new_fileids_list):', len(new_fileids_list))
            # print(type(self._fileids))

            # Update self._fileids to the new list.
            self._fileids = sorted(new_fileids_list)

    def raw(self, fileids=None):

        """
        :return: Returns the text of the specified files as a single string.
        :rtype: str
        """

        # Check if no fileids are specified.
        if (fileids is None):

            # Use the fileids in this corpus.
            fileids = self._fileids

        # Check if the fileids is actually a string.
        elif isinstance(fileids, str):

            # Make a list containing that string.
            fileids = [fileids]

        # Make a list to store the raw texts.
        raw_texts = []

        # Go through each file ID in the list.
        for fileid in fileids:

            # Open the file.
            # TODO: Should use self.open() here from CorpusReader like PlaintextCorpusReader?
            file_in = open(self.root + '/' + fileid, 'r')

            # Read the contents of the file.
            file_text = file_in.read()

            # Close the file.
            file_in.close()

            # Make a JSON object from the text.
            json_object = json.loads(file_text)

            # Set the paper as en empty string.
            paper = ""

            # print(json_object)

            # Check whether to include titles or not.
            if (self._include_titles):
                # Concatenate the title.
                paper += json_object['metadata']['title'] + '\n'

                # print("TITLE: " + json_object['metadata']['title'])

            # Check whether to include abstracts or not.
            if (self._include_abstracts):

                # Make sure there is an entry for the abstract.
                if ('abstract' in json_object):

                    # Go through each section of the abstract.
                    for section in json_object['abstract']:
                        # Concatenate the section.
                        paper += section['text'] + '\n'

            # Check whether to include body_text or not.
            if (self._include_bodies):

                # Go through each section of the paper.
                for section in json_object['body_text']:
                    # Concatenate the section.
                    paper += section['text'] + '\n'

            # Read the contents of the file and append to the list of raw texts.
            raw_texts.append(paper)

        # Concatenate the items in the list and return the result.
        return concat(raw_texts)

    def words(self, fileids=None):
        """
        :return: List of words and punctuation from the specified files.
        :rtype: list(str)
        """

        # print("fileids = ")
        # print(fileids)
        # print("self.abspaths() =")
        # print(self.abspaths(fileids, True, True))

        # Return the concatenation of all the lists.
        return concat(

            # Do a list comprehension.
            [
                self.CorpusView(path, self._read_word_block, encoding=encoding)
                for (path, encoding, fileid) in self.abspaths(fileids, True, True)
            ]
        )

    def sents(self, fileids=None):
        """
        :return: List of sentences from the specified files.
        :rtype: list(list(str))
        """

        # Check that there's a sentence tokenizer.
        if (self._sent_tokenizer is None):
            # Raise an error.
            raise ValueError("No sentence tokenizer for this corpus reader")

        # Return the concatenation of all the lists.
        return concat(

            # Do a list comprehension.
            [
                self.CorpusView(path, self._read_sent_block, encoding=encoding)
                for (path, encoding, fileid) in self.abspaths(fileids, True, True)
            ]
        )

    # TODO: Warning! Currently, paras() treats a section of the paper as a paragraph,
    # which may or may not be acceptable. If we want to work at a paragraph level,
    # we may need to revisit this implementation and make some adjustments.
    def paras(self, fileids=None):
        """
        :return: List of paragraphs, which is each a list of sentences, which is each a list of words.
        :rtype: list(list(list(str)))
        """

        # Check that there's a sentence tokenizer.
        if (self._sent_tokenizer is None):
            # Raise an error.
            raise ValueError("No sentence tokenizer for this corpus reader")

        # Return the concatenation of all the lists.
        return concat(

            # Do a list comprehension.
            [
                self.CorpusView(path, self._read_para_block, encoding=encoding)
                for (path, encoding, fileid) in self.abspaths(fileids, True, True)
            ]
        )

    # def journals(self, fileids = None):
    #     """
    #     :return: List of journals the papers were published in from metadata.csv.
    #     :rtype: list(str)
    #     """

    # def publish_times(self, fileids = None):
    #     """
    #     :return: List of dates the papers were published from metadata.csv.
    #     :rtype: list(str)
    #     """

    # def authors(self, fileids = None):
    #     """
    #     :return: List of authors for the papers from metadata.csv.
    #     For each paper, a list is returned. A paper may have multiple authors.
    #     Or, a paper might not have any authors listed.
    #     :rtype: list(list(str))
    #     """

    # def countries(self, fileids = None):
    #     """
    #     :return: List of countries of the authors for the papers from metadata.csv.
    #     For each paper, a list is returned. A paper may have multiple authors and thus multiple countries.
    #     Or, a paper might not have any authors listed.
    #     :rtype: list(list(str))
    #     """

    # def institutions(self, fileids = None):
    #     """
    #     :return: List of institutions of the authors for the papers from metadata.csv.
    #     For each paper, a list is returned. A paper may have multiple authors and thus multiple institutions.
    #     Or, a paper might not have any authors listed.
    #     :rtype: list(list(str))
    #     """

    def metadata(self, fileids=None, fileids_only=True):
        """
        :return: Dictionary of metadata from metadata.csv for the specified list of files. Set fileids_only = False if you want all metadata (even if the actual paper isn't in the corpus).
        :rtype: dict(list(dict))
        """

        # Check if no fileids are specified.
        if (fileids is None):

            # Use the fileids in this corpus.
            fileids = self._fileids

        # Check if the fileids is actually a string.
        elif isinstance(fileids, str):

            # Make a list containing that string.
            fileids = [fileids]

        # Check if fileids_only is False.
        if (not fileids_only):

            # Make an empty dictionary to hold the metadata.
            metadata_dictionary = defaultdict(list)

            # Open the CSV file.
            csv_file = open(self._metadata_file, 'r', newline='', encoding=self._encoding)

            # Try finding the dialect.
            dialect = csv.Sniffer().sniff(csv_file.read())

            # Reset to the beginning of the file.
            csv_file.seek(0)

            # Setup a CSV reader on the file.
            csv_reader = csv.DictReader(csv_file, dialect=dialect)

            # Go through each row in the metadata.
            for row in csv_reader:
                # Use the cord_uid as the key and append the row.
                # The entries are lists sense a cord_uid can appear in multiple rows.
                metadata_dictionary[row['cord_uid']].append(row)

            # Return the metadata dictionary.
            return metadata_dictionary

        # Otherwise, make a dictionary of just the wanted stuff.
        else:

            # Make an empty dictionary to hold the metadata.
            metadata_dictionary = defaultdict(list)

            # Open the CSV file.
            csv_file = open(self._metadata_file, 'r', newline='', encoding=self._encoding)

            # Try finding the dialect.
            dialect = csv.Sniffer().sniff(csv_file.read())

            # Reset to the beginning of the file.
            csv_file.seek(0)

            # Setup a CSV reader on the file.
            csv_reader = csv.DictReader(csv_file, dialect=dialect)

            # Go through each row in the metadata.
            for row in csv_reader:

                # Check if this entry has a PCM parse file.
                if (row['pmc_json_files'] != ''):
                    # Add the row to the dictionary.
                    metadata_dictionary[row['pmc_json_files']].append(row)

                # Check if this row has a PDF parse file.
                if (row['pdf_json_files'] != ''):

                    # The PDF parses can actually be a list of files.
                    # So, get the list of PDF parse files.
                    pdf_parses_file_list = row['pdf_json_files'].split('; ')

                    # Go through each file.
                    for pdf_parse_file in pdf_parses_file_list:
                        # Add the row to the dictionary.
                        metadata_dictionary[row['pdf_json_files']].append(row)

            # Make an empty dictionary to hold the metadata just for the fileids.
            fileids_metadata_dictionary = defaultdict(list)

            # Go through each fileid.
            for fileid in fileids:
                # Add the entry for this fileid over.
                fileids_metadata_dictionary[fileid] = metadata_dictionary[fileid]

            # Return the metadata for the fileids.
            return fileids_metadata_dictionary

    def statistics(self):
        """
        :return: Nothing. Prints some information about the entries in metadata.csv and files present in the corpus.
        :rtype: ???
        """

        # Open the CSV file.
        csv_file = open(self._metadata_file, 'r', newline='', encoding=self._encoding)

        # Try finding the dialect.
        dialect = csv.Sniffer().sniff(csv_file.read())

        # Reset to the beginning of the file.
        csv_file.seek(0)

        # Setup a CSV reader on the file.
        csv_reader = csv.DictReader(csv_file, dialect=dialect)

        unique_cord_uid_dictionary = {}
        metadata_row_count = 0
        metadata_pdf_count = 0
        metadata_total_pdf_count = 0
        metadata_pmc_count = 0
        metadata_pdf_no_pmc_count = 0
        metadata_pmc_no_pdf_count = 0
        metadata_both_count = 0
        metadata_neither_count = 0

        pdf_parse_has_more = 0
        pmc_parse_has_more = 0
        both_parses_same = 0

        # Go through each row in the metadata.
        for row in csv_reader:

            # Increment the row count.
            metadata_row_count += 1

            # Add the cord_uid to the dictionary.
            unique_cord_uid_dictionary[row['cord_uid']] = 0

            # Check if there is both a PDF parse and a PMC parse for this paper.
            if (row['pdf_json_files'] != '' and row['pmc_json_files'] != ''):
                metadata_both_count += 1

                # This portion takes a long time to run.
                # Compare the PDF parse with the PMC parse and see which has more characters.
                # if (os.path.exists(self._root + row['pdf_json_files']) and os.path.exists(self._root + row['pmc_json_files'])):

                #     # Get contents of the PDF parse.
                #     pdf_parse_file = open(self._root + row['pdf_json_files'], 'r')
                #     pdf_parse_text = pdf_parse_file.read()
                #     pdf_parse_file.close()

                #     # Get contents of the PMC parse.
                #     pmc_parse_file = open(self._root + row['pmc_json_files'], 'r')
                #     pmc_parse_text = pmc_parse_file.read()
                #     pmc_parse_file.close()

                #     # Check which file has more.
                #     if (len(pdf_parse_text) > len(pmc_parse_text)):
                #         pdf_parse_has_more += 1

                #     elif (len(pdf_parse_text) < len(pmc_parse_text)):
                #         pmc_parse_has_more += 1

                #     else:
                #         both_parses_same += 1

            # Check if there is neither a PDF parse and a PMC parse for this paper.
            if (row['pdf_json_files'] == '' and row['pmc_json_files'] == ''):
                metadata_neither_count += 1

            # Check if there is a PDF parse, but a PMC parse for this paper.
            if (row['pdf_json_files'] != '' and row['pmc_json_files'] == ''):
                metadata_pdf_no_pmc_count += 1

            # Check if there is not a PDF parse, but is a PMC parse for this paper.
            if (row['pdf_json_files'] == '' and row['pmc_json_files'] != ''):
                metadata_pmc_no_pdf_count += 1

            # Check if there is both a PDF parse for this paper.
            if (row['pdf_json_files'] != ''):
                metadata_pdf_count += 1

                # Get the list of PDF parse files.
                pdf_parses_file_list = row['pdf_json_files'].split('; ')

                # Check if there's more than one file.
                if (len(pdf_parses_file_list) > 0):

                    # Go through each file.
                    for pdf_parse_file in pdf_parses_file_list:
                        # Increment the count for total number of PDFs parses.
                        metadata_total_pdf_count += 1

            # Check if there is both a PMC parse for this paper.
            if (row['pmc_json_files'] != ''):
                metadata_pmc_count += 1

        # Print information about corpus from metadata.csv.
        print('metadata.csv:')
        print('\tRows:', metadata_row_count)
        print('\tUnique cord_uids:', len(unique_cord_uid_dictionary.items()))
        print('\tRows with PDF Parses:', metadata_pdf_count)
        print('\tRows with PMC Parses:', metadata_pmc_count)
        print('\tRows with PDF Parses and No PMC Parses:', metadata_pdf_no_pmc_count)
        print('\tRows with PMC Parses and No PDF Parses:', metadata_pmc_no_pdf_count)
        print('\tRows with Both:', metadata_both_count)
        print('\tRows with Neither:', metadata_neither_count)
        print('\tTotal PDF Parse File:', metadata_total_pdf_count)

        # Print information for the parse directories.
        print('Parse Directories:')
        pdf_parse_list = os.listdir(self._root + 'document_parses/pdf_json/')
        print('\tpdf_json:', len(pdf_parse_list))
        pmc_parse_list = os.listdir(self._root + 'document_parses/pmc_json/')
        print('\tpmc_json:', len(pmc_parse_list))
        # print('\tpdf_parse_has_more:', pdf_parse_has_more)
        # print('\tpmc_parse_has_more:', pmc_parse_has_more)
        # print('\tboth_parses_same:', both_parses_same)

    def citations(self, fileids=None):
        """
        :return: Returns the citations for a fileid, list of fileids, or all the fileids.
        :rtype: dict(dict)
        """

        # Check if no fileids are specified.
        if (fileids is None):

            # Use the fileids in this corpus.
            fileids = self._fileids

        # Check if the fileids is actually a string.
        elif isinstance(fileids, str):

            # Make a list containing that string.
            fileids = [fileids]

        # Make a dictionry to store the raw texts.
        citations_dictionary = {}

        # Go through each file ID in the list.
        for fileid in fileids:

            # Open the file.
            # TODO: Should use self.open() here from CorpusReader like PlaintextCorpusReader?
            file_in = open(self.root + '/' + fileid, 'r')

            # Read the contents of the file.
            file_text = file_in.read()

            # Close the file.
            file_in.close()

            # Make a JSON object from the text.
            json_object = json.loads(file_text)
            # print(str(json_object))

            # Put an empty dictionary for this entry.
            citations_dictionary[fileid] = {}

            # print(json_object)

            # Check whether this JSON object has a key for the citations.
            if ('bib_entries' in json_object):
                # Concatenate the title.
                citations_dictionary[fileid] = json_object['bib_entries']

        # Concatenate the items in the list and return the result.
        return citations_dictionary

    # This function is used by words() in conjunction with the StreamBackedCorpusView class.
    # Basically, it defines how to read a chunk of words from the corpus.
    # Currently, it's implemented to read the entire contents of a paper at a time.
    def _read_word_block(self, stream):

        # Make an empty list to hold the words.
        word_list = []

        # Grab the contents of the file.
        file_text = stream.read()

        # Make a JSON object from the text.
        json_object = json.loads(file_text)

        # TODO: Decide what parts to include in the text.
        # TODO: Include title? Abstract? Bibliography?
        # TODO: Maybe have options to specify what to include?

        # Set the paper as en empty string.
        paper = ""

        # Check whether to include titles or not.
        if (self._include_titles):
            # Concatenate the title.
            paper += json_object['metadata']['title'] + '\n'

            # print("TITLE: " + json_object['metadata']['title'])

        # Check whether to include abstracts or not.
        if (self._include_abstracts):

            # Make sure there is an entry for the abstract.
            if ('abstract' in json_object):

                # Go through each section of the abstract.
                for section in json_object['abstract']:
                    # Concatenate the section.
                    paper += section['text'] + '\n'

        # Check whether to include body_text or not.
        if (self._include_bodies):

            # Go through each section of the paper.
            for section in json_object['body_text']:
                # TODO: Should newlines be being added to the end?
                # Concatenate the section.
                paper += section['text']

        # Tokenize the paper and add the tokens to the list of words.
        word_list.extend(self._word_tokenizer.tokenize(paper))

        # Return the list of words.
        return word_list

    def _read_sent_block(self, stream):

        # Make an empty list to hold the sentences.
        sentence_list = []

        # Grab the contents of the file.
        file_text = stream.read()

        # Make a JSON object from the text.
        json_object = json.loads(file_text)

        # TODO: Decide what parts to include in the text.
        # TODO: Include title? Abstract? Bibliography?
        # TODO: Maybe have options to specify what to include?

        # Check whether to include titles or not.
        if (self._include_titles):
            # Add the list comprehension to the list of sentences.
            sentence_list.extend(
                [
                    # Add the list of words in this sentece.
                    self._word_tokenizer.tokenize(sentence)

                    # And do that for each sentence in this section of the paper.
                    for sentence in self._sent_tokenizer.tokenize(json_object['metadata']['title'])
                ]
            )

        # Check whether to include abstracts or not.
        if (self._include_abstracts):

            # Make sure there is an entry for the abstract.
            if ('abstract' in json_object):

                # Go through each section of the abstract.
                for section in json_object['abstract']:
                    # Add the list comprehension to the list of sentences.
                    sentence_list.extend(
                        [
                            # Add the list of words in this sentence.
                            self._word_tokenizer.tokenize(sentence)

                            # And do that for each sentence in this section of the paper.
                            for sentence in self._sent_tokenizer.tokenize(section['text'])
                        ]

                    )

        # Check whether to include body_text or not.
        if (self._include_bodies):

            # Go through all the sections in the paper.
            for section in json_object['body_text']:
                # Add the list comprehension to the list of sentences.
                sentence_list.extend(
                    [
                        # Add the list of words in this sentence.
                        self._word_tokenizer.tokenize(sentence)

                        # And do that for each sentence in this section of the paper.
                        for sentence in self._sent_tokenizer.tokenize(section['text'])
                    ]

                )

        # Return the list of sentences.
        return sentence_list

    def _read_para_block(self, stream):

        # Make an empty list to hold the paragraphs.
        paragraph_list = []

        # Grab the contents of the file.
        file_text = stream.read()

        # Make a JSON object from the text.
        json_object = json.loads(file_text)

        # Check whether to include titles or not.
        if (self._include_titles):
            # Add the list comprehension to the list of sentences.
            paragraph_list.append(
                [
                    # Add the list of words in this sentece.
                    self._word_tokenizer.tokenize(sentence)

                    # And do that for each sentence in this section of the paper.
                    for sentence in self._sent_tokenizer.tokenize(json_object['metadata']['title'])
                ]
            )

        # Check whether to include abstracts or not.
        if (self._include_abstracts):

            # Make sure there is an entry for the abstract.
            if ('abstract' in json_object):

                # Go through each section of the abstract.
                for section in json_object['abstract']:
                    # Add the list comprehension to the list of sentences.
                    paragraph_list.append(
                        [
                            # Add the list of words in this sentence.
                            self._word_tokenizer.tokenize(sentence)

                            # And do that for each sentence in this section of the paper.
                            for sentence in self._sent_tokenizer.tokenize(section['text'])
                        ]

                    )

        # Check whether to include body_text or not.
        if (self._include_bodies):

            # Go through all the sections in the paper.
            for section in json_object['body_text']:
                # Add the list comprehension to the list of paragraphs.
                paragraph_list.append(
                    [
                        # Add the list of words in this sentence.
                        self._word_tokenizer.tokenize(sentence)

                        # And do that for each sentence in this section of the paper.
                        for sentence in self._sent_tokenizer.tokenize(section['text'])
                    ]

                )

        # Return the list of paragraphs.
        return paragraph_list
