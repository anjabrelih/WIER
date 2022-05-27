import os
import nltk
#nltk.download()
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from stopwords import stop_words_slovene

#from html.parser import HTMLParser

#tokens_all = []

#class RR_HTMLParse(HTMLParser):
 #   def handle_starttag(self, tag: str, attrs: list[tuple[str]]) -> None:
  #      #return super().handle_starttag(tag, attrs)
   #     tokens_all.append(["starttag",tag])
    #    #print("starttag: ",tag)

    #def handle_endtag(self, tag) -> None:
     #   #return super().handle_endtag(tag)
      #  tokens_all.append(["endtag",tag])
       # #print("endtag: ",tag)

    #def handle_data(self, data: str) -> None:
    #    #return super().handle_data(data)
     #   if data != ' ':
      #      tokens_all.append(["data", data])
       #     print("data: ", data)

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
def index_words(html, doc):


    # Tokenize html file (set it to lowercase)
    tokens = nltk.word_tokenize(html.text.lower())
    print(tokens)
    print(len(tokens))
    #print ("END of uncleaned tokens ------------")

    # Activate parser
    #parser = RR_HTMLParse()

    # Get tokens
    #input_tokens = []
    #parser.feed(html)
    #tokens_alltags = list(tokens_all)
    #tokens_all.clear()
    #if tokens_alltags[0] == "data":
    #    input_tokens.append(tokens_alltags[1])
    #print(input_tokens)

    #tokens = []
    #for input in input_tokens:
    #    part_tokens = nltk.word_tokenize(input.lower())
    #    tokens.append(part_tokens)
    
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
    
    print(cleaned_tokens)
    print(len(cleaned_tokens))


    checked_tokens = []
    for t in cleaned_tokens:

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

        #print("token: ", t, " index: ", index, " freq: ", freq)

        # Write to db
        #insert_data(t, doc, freq, str(index))


        
        


# Iterate over folders in input-indexing
input_indexing = ["../input-indexing/e-prostor.gov.si","../input-indexing/e-uprava.gov.si","../input-indexing/evem.gov.si","../input-indexing/podatki.gov.si"]
for folder in input_indexing:
    # Interate over files
    for file in os.listdir(folder):
        if file.endswith(".html"):
            path = os.path.join(folder,file)
            #file_r = open(path, 'r', encoding="utf8")
            #html = BeautifulSoup(file_r.read(), 'lxml')

            #index_words(html, file)

## OUT
path = "../input-indexing/e-prostor.gov.si/e-prostor.gov.si.1.html"
file = open(path, 'r', encoding="utf8")
html = BeautifulSoup(file.read(), 'lxml')
#html = codecs.open(path, "r","utf-8").read()
filename = "e-prostor.gov.si.1.html"


index_words(html, filename)
## end - OUT


# End - close the connection
#conn.close()
