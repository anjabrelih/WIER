import os
import nltk
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from stopwords import stop_words_slovene
import sys
import time

# Set number of results and snippets in the output
NO_SNIPPETS = 5
NO_RESULTS = 4

folder = "../input-indexing/"

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

    # Tokenize html file (don't use lowercase at this point - it's used for output)
    tokens = nltk.word_tokenize(html.text.lower())
    #print(tokens)

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

    page = []
    checked_tokens = []
    index = []
    freq = int(0)
    for t in tokens:

        if t in query:

            # Check if token was already checked
            if t in checked_tokens:
                continue
            else:
                checked_tokens.append(t)

            # Check all tokens for iterations
            for i in range(len(tokens)):
                if tokens[i] == t:
                    index.append(i)
                    freq += 1


    if freq != 0:
        page = [doc, freq, index]
    
    return page

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

                #print("Searching file: ", file)
                page = search_page(html, file, query)

                if page != []:
                    pages.append(page)

    # Sort - descending          
    pages.sort(key=lambda c: c[1], reverse=True)

    return pages, len(pages)

def format_output(data, query):

    snippets = []
    doc = []

    # Format results and snippets
    for i, row in enumerate(data):
        # Correct document names (add folder - i didn't store this in db)
        if row[0].startswith("e-prostor"):
            document = "e-prostor.gov.si/"+row[0]
        if row[0].startswith("e-uprava"):
            document = "e-uprava.gov.si/"+row[0]
        if row[0].startswith("evem"):
            document = "evem.gov.si/"+row[0]
        if row[0].startswith("podatki"):
            document = "podatki.gov.si/"+row[0]
        doc.append(document)

        # read the document
        path = os.path.join(folder,document)
        file_r = open(path, 'r', encoding="utf8")
        html = BeautifulSoup(file_r.read(), features="lxml").getText(separator=" ")
          

        # Tokenize html file (don't set it to lower because it's used for snippets!)
        tokens = nltk.word_tokenize(html)
        #print(tokens)


        # Format snippets
        snippets_doc = format_snippets(query, tokens)
        snippets.append(snippets_doc)
        # Format only n snippets
        if i == NO_RESULTS:
            break
        


    return snippets, doc

def format_snippets(query, tokens):
    snippets = ""
    
    index = []
    for q in query:
        # If stopwords in query - don't use them
        if q not in stop_words_slovene:
            for i in range(len(tokens)):
                # Use lower here (dont overwrite tokens)
                if tokens[i].lower() == q.lower():
                    index.append(i)

    

    for i, idx in enumerate(index):
        
        # Set down range
        if idx == 0:
            limit_d = 0
        elif idx - 1 == 0:
            limit_d = 1
        elif idx -2 == 0:
            limit_d = 2
        else:
            limit_d = 3

        # Set upper range
        if idx + 3 <= len(tokens):
            limit_u = 3
        elif idx + 2 <= len(tokens):
            limit_u = 2
        elif idx + 3 <= len(tokens):
            limit_u = 2
        else:
            limit_u = 0

        # Get tokens for snippets
        snippets += " ".join(tokens[idx - limit_d:idx + limit_u])


        # Remove unvated chars
        snippets = snippets.replace(" , ",", ")
        snippets = snippets.replace(" . ",". ")
        snippets = snippets.replace(" ( "," (")
        snippets = snippets.replace(" ) ",") ")
        snippets = snippets.replace("., ",". ")
        snippets = snippets.replace(" ? ","? ")
        snippets = snippets.replace(" ! ","! ")
        snippets = snippets.replace(" : ",": ")
        snippets = snippets.replace("  "," ")
        if snippets.startswith(")"):
            snippets = snippets[1:]
        snippets = snippets.replace("  "," ")
        if snippets.endswith("("):
            snippets = snippets[:-1]

        # Set ... (start)
        if idx != 0 and i == 0:
            snippets = " ... " + snippets
        
        # Set ... except if it ends
        if idx == len(tokens):
            pass
        else:
            snippets += " ... "

        # Limit number of snippets (set above as global)
        if i == NO_SNIPPETS:
            break

    return snippets


if __name__ == '__main__':
    input_query = sys.argv[1:]

    # Start timer
    start_time = time.time()

    # set all words to lowercase
    query = []
    for q in input_query:
        # If stopwords in query - don't use them for search
        if q not in stop_words_slovene:
            query.append(q.lower())

    # basic search
    output, n_results = basic_search(query)

    # Format output
    snippets, doc = format_output(output, input_query)
    #print(snippets)


    # Stop timer
    search_time = (time.time() - start_time)*1000 # [ms]
    

    # Print result
    print("Results for a query: \"{}\"".format(" ".join(input_query)),"\n\n\t{} results found in {} ms.".format(n_results,round(search_time,2)))
    print("\n\n\tFrequencies\tDocument\t\t\t\t\tSnippet")
    print("\t-----------\t-------------------------------------------\t-----------------------------------------------------------")
    for i, row in enumerate(output):
 
        print("\t{}".format(row[1]),"\t\t{}".format(doc[i]),"\t\t{}".format(snippets[i]))
        
        # Print only top set n results
        if i == NO_RESULTS:
            break