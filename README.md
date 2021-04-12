
# Table of Contents

1.  [CORD-19 Corpus Reader](#cord-19-corpus-reader)
    1.  [About](#about)
    2.  [Dataset Format](#dataset-format)
    3.  [Examples](#examples)
        1.  [Creating a Corpus Reader](#creating-a-corpus-reader)
        2.  [Creating a Corpus Reader to Read Only Bodies of Papers](#creating-a-corpus-reader-to-read-only-bodies-of-papers)
        3.  [Creating a Corpus Reader Preferring PMC Parses of Papers](#creating-a-corpus-reader-preferring-pmc-parses-of-papers)
        4.  [Getting a List of Documents in the Corpus](#getting-a-list-of-documents-in-the-corpus)
        5.  [Getting All the Words in the Corpus](#getting-all-the-words-in-the-corpus)
        6.  [Getting All the Words From Specific Documents in the Corpus](#getting-all-the-words-from-specific-documents-in-the-corpus)
        7.  [Getting Metadata for Specific Documents in the Corpus](#getting-metadata-for-specific-documents-in-the-corpus)
        8.  [Display Statistics About the Corpus](#display-statistics-about-the-corpus)
        9.  [Plotting 50 Most Common Words from 10000 Documents](#plotting-50-most-common-words-from-10000-documents)
        10. [Plotting 50 Most Popular Days to Publish](#plotting-50-most-popular-days-to-publish)
    4.  [Tasks](#tasks)
        1.  [To Do](#to-do)
        2.  [In Progress](#in-progress)
        3.  [Done](#done)
    5.  [Questions](#questions)
    6.  [Issues](#issues)


<a id="cord-19-corpus-reader"></a>

# CORD-19 Corpus Reader


<a id="about"></a>

## About

The `CORD19CorpusReader` class is a corpus reader for the CORD-19 corpus
(<https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge>).
The idea is to be able to load the CORD-19 corpus into NLTK. This project
was originally created for Natural Language Processing (NLP) coursework
at the University of Missouri by Jason James, Alex Morehead, and others.

Documents in the CORD-19 corpus are stored as JSON files. Since the
documents are in JSON, the parts of the paper are separated out.
Currently, when setting up the corpus reader, you can specify which
parts of the papers you want to access: titles, abstracts, and / or
bodies with the flags `include_titles`, `include_abstracts`, and
`include_bodies`. For example, in some situations, you might really only
care about the body of the paper, which contains most of the text. In
other situations, you might just want the abstracts. By default, titles,
abstracts, and bodies are included.

For some papers, there are both PDF parses and PMC parses. To indicate
which is preferred, the corpus reader has a `prefer_pdf_parses`
parameter and a `prefer_pmc_parses` parameter. In cases where both
parses are available, the `prefer_pdf_parses` tells the reader to choose
the PDF parses when set to `True` and the `prefer_pmc_parses` parameter
tells the corpus reader to choose the PMC parse when set to `True`. If
both are set to `True`, it just uses all the JSON files, which is
actually a bit faster since it does not have to perform deduplication.
If both are set to `False` (which is not something you would probably
want to do in actuality), it would basically exclude either parse of a
paper when there&rsquo;s a duplicate. By default, `prefer_pdf_parses` is set
to `True` and `prefer_pmc_parses` is set to `False`.

Currently, `raw()`, `words()`, `sents()`, and `paras()` have
implementations and basically work like would be expected using NLTK.
Right now, these functions are just returning the text body of the
papers, but the intent is to be able to specify in the reader which
parts of the paper to return (title, abstract, body, and bibliography).
In fair warning, it should also be noted that currently `paras()` is
treating a section of the paper as a paragraph, which may or may not be
an acceptable treatment of paragraphs, so if we really need to work at
the paragraph level, we may want to revisit the implementation details
of `paras()`.

There&rsquo;s a few options for inputs into `raw()`, `words()`, `sents()`, and
`paras()`: a file ID as a string does the operation on just the
corresponding document, a list of file IDs does the operation on just
the corresponding documents, and no arguments performs the operation on
all the documents in the corpus.

The corpus is very large, so operations can take a while to complete
when performed on the entire corpus. For example, it took about 30
minutes to store the output from `words()` to a list and print the
length of the list. To convert the list to a set and print the length of
the set took about another 10 minutes.

Metadata for papers is stored in a file called `metadata.csv` in the
root directory of the corpus. Basically, each row of the file is the
metadata for a particular paper. So far, there&rsquo;s an initial
implementation of `metadata()` that can be used to retrieve the metadata
for papers. Similar to the above methods, either a string of a file ID
or a list of file IDs can be input to `metadata()` to retrieve the
corresponding metadata for those documents. Additionally, passing in no
arguments returns the metadata for all the documents in the corpus.
There&rsquo;s also a parameter `fileids_only` that specifies whether to return
metadata for only papers actually in the corpus when set to `True` or
all the metadata available (even for papers whose parses aren&rsquo;t in the
corpus) when set to `False`. The default value for `fileids_only` is
`True`. When `fileids_only` is `True`, the metadata is returned as a
dictionary, with the fileids as keys, of lists, where an entry in the
list is itself a dictionary representing a row from `metadata.csv`.
However, when `fileids_only` is set to `False`, the metadata returned is
a dictionary, with the cord<sub>uid</sub> as the keys, of lists, where each entry
in the list is itself a dictionary representing a row from
`metadata.csv`. The reason for the discrepency is that there might be a
want to correlate metadata with its corresponding paper, in which case
indexing into the metadata with the paper&rsquo;s fileid seems intuitive. On
the other hand, for metadata for papers for which there is no
corresponding fileid, there&rsquo;s not really a lot of options for what to
index into it with, so teh cord<sub>uid</sub> is used.

`test_coord19.py` contains some rudimentary tests using methods in the
`CORD19CorpusReader` class to display the output of the methods.


<a id="dataset-format"></a>

## Dataset Format

The dataset is updated pretty regularly on Kaggle. So, the exact number
of papers can change on a daily basis.

Inside the root directory of the dataset is a metadata file called
`metadata.csv`. Each row represents a particular paper and has a
`cord_uid` that serves as a sort of key for that paper. Note that the
`cord_uid=s are not unique in =metadata.csv`: multiple rows might have
the same `cord_uid`, but contain differening data (it usually looks like
one of the entries is more complete than the other). If a paper has a
PMC parse, there will be an entry for the filename in the
`pmc_json_files` column. Similarly, if the paper has a PDF parse, there
will be an entry for its filename in the `pdf_json_files` column.
However, sometimes multiple files might be listed in the
`pdf_json_files` column: apparently, one corresponds to the main article
and the others contain related matter and so these types of entries are
represented as a `;` separated list (semicolon and space).

Inside the directory for the dataset, there is a directory called
`document_parses`. Inside of `document_parses`, there are two folders
called `pdf_json` and `pmc_json`. The files in these folders are the
actual data from the papers in JSON format. Some papers only have a PDF
parse and some papers only have a PMC parse and some papers have both a
PDF and a PMC parse and some papers have neither a PDF parse nor a PMC
parse.


<a id="examples"></a>

## Examples


<a id="creating-a-corpus-reader"></a>

### Creating a Corpus Reader

    # Import the CORD19CorpusReader class.
    from cord19 import CORD19CorpusReader
    
    # Directory of the CORD-19 corpus.
    # Assumes the repository directory is sibling to / at the same level as the corpus directory.
    # Also assumes in the same directory as cord19.py.
    root = '../../../../551982-1490480-bundle-archive/'
    
    # Make a corpus reader on everything that is a .json file in the directory.
    reader = CORD19CorpusReader(root, '.*\.json')


<a id="creating-a-corpus-reader-to-read-only-bodies-of-papers"></a>

### Creating a Corpus Reader to Read Only Bodies of Papers

    # Assume CORD19CorpusReader has been imported and root has been specified.
    
    # By default include_titles, include_abstracts, and include_bodies are all True.
    reader = CORD19CorpusReader(root, '.*\.json', include_titles = False, include_abstracts = False, include_bodies = True)


<a id="creating-a-corpus-reader-preferring-pmc-parses-of-papers"></a>

### Creating a Corpus Reader Preferring PMC Parses of Papers

    # Assume CORD19CorpusReader has been imported and root has been specified.
    
    # When there's both a PDF parse and a PMC parse available for a paper, choose the PMC parse.
    reader = CORD19CorpusReader(root, '.*\.json', prefer_pmc_parses = True, prefer_pdf_parses = False)


<a id="getting-a-list-of-documents-in-the-corpus"></a>

### Getting a List of Documents in the Corpus

    document_list = reader.fileids()


<a id="getting-all-the-words-in-the-corpus"></a>

### Getting All the Words in the Corpus

    # Note that this could take a while since the corpus is quite large.
    word_list = reader.words()


<a id="getting-all-the-words-from-specific-documents-in-the-corpus"></a>

### Getting All the Words From Specific Documents in the Corpus

    # Make a list of documents of interest.
    document_list = ['document_parses/pdf_json/0000028b5cc154f68b8a269f6578f21e31f62977.json',
    'document_parses/pmc_json/PMC7480786.xml.json']
    
    # Retrieves words from only the specified documents.
    word_list = reader.words(document_list)


<a id="getting-metadata-for-specific-documents-in-the-corpus"></a>

### Getting Metadata for Specific Documents in the Corpus

    # Make a list of documents of interest.
    document_list = ['document_parses/pdf_json/0000028b5cc154f68b8a269f6578f21e31f62977.json',
    'document_parses/pmc_json/PMC7480786.xml.json']
    
    # Retrieves metadata from metadata.csv for only the specified documents.
    metadata_dictionary = reader.metadata(document_list)


<a id="display-statistics-about-the-corpus"></a>

### Display Statistics About the Corpus

    # Displays information about rows in metadata.csv and counts of document parse folders.
    reader.statistics()


<a id="plotting-50-most-common-words-from-10000-documents"></a>

### Plotting 50 Most Common Words from 10000 Documents

    # Grab a list of stopwords.
    stopword_list = nltk.corpus.stopwords.words('english')
    
    # Make a list of punctuation and uninteresting items that might show up in a paper.
    ignore_list = ['.', ',', '!', '?', '[', ']', '(', ')', '`', '"', '\'', ';', ':', '%', '-', '+', '=', '_', '),', ').', '],', '/', '\\', '.,', 'et', 'al']
    
    # Concatenate the lists.
    ignore_list = ignore_list + stopword_list
    
    # Grab 10k documents.
    document_list = reader.fileids()[0:10000]
    
    # Make a word list of words in the documents, but not in the ignore list.
    word_list = [word.lower() for word in reader.words(document_list) if word.lower() not in ignore_list]
    
    # Create a frequency distribution of th words.
    frequency_distribution = nltk.FreqDist(word_list)
    
    # Plot the distribution of the 50 most common words.
    frequency_distribution.plot(50)

![img](images/freqdist_top50words.png "Frequency Distribution of Most Common 50 Dates")


<a id="plotting-50-most-popular-days-to-publish"></a>

### Plotting 50 Most Popular Days to Publish

    # Grab the metadata.
    metadata = reader.metadata()
    
    # Make an empty list of publish times.
    publish_times = []
    
    # Go through each item in the metadata.
    for (key, entry_list) in metadata.items():
    
        # Go through each entry in the list.
        for entry in entry_list:
    
            # Add the publish time to the list.
            publish_times.append(entry['publish_time'])
    
    # Make a frequency distribution on the list of publish times.
    frequency_distribution = nltk.FreqDist(publish_times)
    
    # Plot the 50 most popular days to publish on.
    frequency_distribution.plot(50)

![img](images/freqdist_top50days.png "Frequency Distribution of Most Common 50 Dates")


<a id="tasks"></a>

## Tasks


<a id="to-do"></a>

### To Do

-   Add functions to retrieve specific pieces of metadata
    -   Implement `journals()` to pull journals metadata
    -   Implement `authors()` to pull authors metadata
    -   Implement `publish_times()` to pull publish times metadata
    -   Implement `countries()` to pull countries (from authors metadata)
        metadata
    -   Implement `institutions()` to pull pull institutions (from authors
        metadata) metadata

-   Add ability to specify which parts of paper to read (title, abstract,
    body, bibliography)
    -   Add `include_bibliographies` flag to indicate whether to include
        bibiliographies at the end of papers
        -   Is this needed and what parts of the bibliographies to include?


<a id="in-progress"></a>

### In Progress


<a id="done"></a>

### Done

-   Do initial implementation of `CORD19CorpusReader` class :jason:
    -   Implement `raw()` :jason:
    -   Implement `words()` :jason:
    -   Implement `sents()` :jason:
    -   Implement `paras()` :jason:

-   Add ability to specify which parts of paper to read (title, abstract,
    and body) :jason:
    -   Add `include_titles` flag to indicate whether to include paper
        titles :jason:
    -   Add `include_abstracts` flag to indicate whether to include paper
        abstracts :jason:
    -   Add `include_bodies` flag to indicate whether to include the actual
        text bodies of papers :jason:

-   Implement `metadata()` to pull entire metadata blocks from
    `metadata.csv` :jason:
-   Implement `statistics()` to display some simple statistics about the
    corpus :jason:
-   Add preferences for deduplication of papers (i.e., don&rsquo;t include both
    PDF parse and PMC parse of the same paper) :jason:


<a id="questions"></a>

## Questions

-   Why do some papers have both PDF and PMC parses?
-   Are PDF and PMC parses of the same paper the same?
-   If a JSON file has an abstract, authors, etc., is that metadata also
    in metadata.csv and vice versa?
-   Is the overlapping metadata (e.g., abstracts) in the JSON files and
    metadata.csv the same?

<div class="rmk" id="org2beec82">
<p>
Boy, I wish I knew.  We would need to compare each pair point by point to
be sure.
</p>

<p>
I suspect it really just reflects the origin of the papers &#x2014; scooped from
open access journals or from PubMed&rsquo;s free text links.  I&rsquo;m surprised there
aren&rsquo;t any notes about methodoloy in the CORD-19 data set itself.
</p>

</div>


<a id="issues"></a>

## Issues

-   Operations can take a long time because of the size of the corpus
-   Metadata availability seems to vary between files
-   Corpus is updated frequently, so different versions may give different
    results
-   Some papers seem to appear twice, as both a PDF parse and a PMC parse

