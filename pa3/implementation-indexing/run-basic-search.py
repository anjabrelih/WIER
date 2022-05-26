import os
import nltk
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from stopwords import stop_words_slovene
import sys
import time

# tokens blacklist
blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    'style',
    'style=',
    'img',
    'src=',
    'footer',
    '»',
    '«',
    '...',
    '©',
    '--',
    '•',
    # https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
]

# Index words in html file
def search_page(html, doc, query):

    # Tokenize html file (set it to lowercase)
    tokens = nltk.word_tokenize(html.text.lower())
        
    # Remove unwanted tokens
    cleaned_tokens = []
    for token in tokens:
        # Remove stopwords - slovene
        if token not in stop_words_slovene:
            # Remove stopwords - english
            if token not in stopwords.words('english'):
                # Remove punctuation
                if token not in string.punctuation:
                    # Remove tokens on blacklist
                    if token not in blacklist:
                            cleaned_tokens.append(token)
    
    #print(cleaned_tokens)
    #print(len(cleaned_tokens))


    checked_tokens = []
    posting = []
    for t in cleaned_tokens:

        if t in query:

            # Check if token was already inserted in db
            if t in checked_tokens:
                continue
            else:
                checked_tokens.append(t)

            # Check all tokens for iterations
            index = []
            freq = int(0)
            for i in range(len(cleaned_tokens)):
                if cleaned_tokens[i] == t:
                    index.append(i)
                    freq += 1

            posting.append(t, doc, freq, index)
            #print("token: ", t, " index: ", index, " freq: ", freq)
    if posting == []:
        return None
    else:
        return posting

def basic_search(query):
    pages = []
    # Iterate over folders in input-indexing
    input_indexing = ["../input-indexing/e-prostor.gov.si","../input-indexing/e-uprava.gov.si","../input-indexing/evem.gov.si","../input-indexing/podatki.gov.si"]
    for folder in input_indexing:
        # Interate over files
        for file in os.listdir(folder):
            if file.endswith(".html"):
                path = os.path.join(folder,file)
                file_r = open(path, 'r', encoding="utf8")
                html = BeautifulSoup(file_r.read(), 'lxml')

                posting = search_page(html, file, query)

                if posting is not None:
                    pages.append(posting)

    # Order?
    return pages


if __name__ == '__main__':
    query = sys.argv[1]

    # !! handle multiple words

    # basic search
    start_time = time.time()
    output = basic_search(query)
    search_time = time.time() - start_time

    # rabis 5 zadetkov, 6 snippetov (če obstajajo?)
    for row in output:
        print(f"\tHits: {row[1]}\n\t\tDoc: '{row[0]}'\n\t\tIndexes: {row[2]}")
