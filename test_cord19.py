################################################################################
#                                                                              #
#    CS 7740/8740                                                              #
#    Fall 2020 - Spring 2021                                                   #
#                                                                              #
#    Class Project - Test CORD-19 Corpus Reader                                #
#    test_cord19.py                                                            #
#                                                                              #
#    Started: Jason James                                                      #
#    2020-9-15                                                                 #
#                                                                              #
#    Modified: Alex Morehead                                                   #
#    2021-4-11                                                                 #
#                                                                              #
################################################################################

from cord19 import CORD19CorpusReader

# Directory of the CORD-19 corpus.
# Assumes the repository directory is sibling to / at the same level as the corpus directory.
root = '../../../Data/Archive/'

# Make a corpus reader on everything that is a .json file in the directory.
reader = CORD19CorpusReader(root, '.*\.json')

# Setup a reader that prefers PMC parses over PDF parses when both are available.
# reader = CORD19CorpusReader(root, '.*\.json', prefer_pdf_parses = False, prefer_pmc_parses = True)

# Setup a reader with both preferences set to True, should just take all the JSON files found.
# reader = CORD19CorpusReader(root, '.*\.json', prefer_pdf_parses = True, prefer_pmc_parses = True)

# Setup a reader with both preferences set to False, which should not include either when there's duplicates (which is probably not something you would typically want to do).
# reader = CORD19CorpusReader(root, '.*\.json', prefer_pdf_parses = False, prefer_pmc_parses = False)

# Setup a reader to read only titles.
# reader = CORD19CorpusReader(root, '.*\.json', include_titles = True, include_abstracts = False, include_bodies = False)

# Setup a reader to read only abstracts.
# reader = CORD19CorpusReader(root, '.*\.json', include_titles = False, include_abstracts = True, include_bodies = False)

# Setup a reader to read only bodies.
# reader = CORD19CorpusReader(root, '.*\.json', include_titles = False, include_abstracts = False, include_bodies = True)

# Let's make a variable of a string of a particular file ID.
just_one_document = 'document_parses/pmc_json/PMC7480786.xml.json'

# Let's make a list of a few file IDs.
several_documents = ['document_parses/pdf_json/0000028b5cc154f68b8a269f6578f21e31f62977.json',
                     'document_parses/pdf_json/0001418189999fea7f7cbe3e82703d71c85a6fe5.json',
                     'document_parses/pmc_json/PMC7480774.xml.json',
                     'document_parses/pmc_json/PMC7480786.xml.json']

print('Test fileids()')
print(reader.fileids())
print('len(reader.fileids():', len(reader.fileids()))

print()

print('Test raw() with One File ID')
print(reader.raw(just_one_document))

print()

print('Test raw() with List of File IDs')
print(reader.raw(several_documents))

print()

print('Test words() with One File ID')
print(reader.words(just_one_document))
# for word in reader.words(just_one_document):
#     print(word)

print()

print('Test words() with List of File IDs')
print(reader.words(several_documents))

print()

print('Test sents() with One File ID')
print(reader.sents(just_one_document))
# for sentence in reader.sents(just_one_document)[0:5]:
#     print(sentence)

print()

print('Test sents() with List of File IDs')
print(reader.sents(several_documents))

print()

print('Test paras() with One File ID')
print(reader.paras(just_one_document))
# for paragraph in reader.paras(just_one_document)[0:5]:
#     print(paragraph)

# print('Test paras() with List of File IDs')
# print(reader.paras(several_documents))
# words = reader.words()
# print("Word Count:", len(words))

print('Test metadata() with One File ID')
print(reader.metadata(just_one_document))

print()

print('Test metadata() with List of File IDs')
print(reader.metadata(several_documents))

print()

print('Test metadata() for Entire Corpus')
metadata = reader.metadata()
# print(reader.metadata())
print('len(metadata.items()):', len(metadata.items()))
# # print('cord_id(8s9y5io9):', all_metadata['document_parses/pdf_json/46c6bbfc98d4485c31d8bdc82cbc8eaee4d31eb0.json'])

print()

print('Test metadata() for All Metadata')
# print(reader.metadata())
metadata = reader.metadata(fileids_only=False)
print('len(metadata.items()):', len(metadata.items()))

print()

print('Test statistics()')
reader.statistics()

print()

print('Test citations() with One File ID')
citations_list = reader.citations(just_one_document)
print(citations_list)

print()

print('Test citations() with List of File IDs')
citations_list = reader.citations(several_documents)
print(citations_list)

print()

# print('Test citations() with All File IDs')
# citations_list = reader.citations()

# print()

# print('Demo Frequency Distribution of Publish Times')
# metadata = reader.metadata()
# publish_times = []
# for (key, entry_list) in metadata.items():
#     for entry in entry_list:
#         publish_times.append(entry['publish_time'])
# # print(publish_times)
# frequency_distribution = nltk.FreqDist(publish_times)
# frequency_distribution.plot(50)

# print()

# print('Demo Frequency Distribution of Publish Times (fileids_only = False)')
# metadata = reader.metadata(fileids_only = False)
# publish_times = []
# for (key, entry_list) in metadata.items():
#     for entry in entry_list:
#         publish_times.append(entry['publish_time'])
# # print(publish_times)
# frequency_distribution = nltk.FreqDist(publish_times)
# frequency_distribution.plot(50)

# print('Demo Frequency Distribution of Most Common Words')
# stopword_list = nltk.corpus.stopwords.words('english')
# ignore_list = ['.', ',', '!', '?', '[', ']', '(', ')', '`', '"', '\'', ';', ':', '%', '-', '+', '=', '_', '),', ').', '],', '/', '\\', '.,', 'et', 'al']
# ignore_list = ignore_list + stopword_list
# document_list = reader.fileids()[0:1000]
# word_list = [word.lower() for word in reader.words(document_list) if word.lower() not in ignore_list]
# frequency_distribution = nltk.FreqDist(word_list)
# frequency_distribution.plot(50)

# print()


# vocabulary = set(words)
# print("Vocabulary Count:", len(vocabulary))
