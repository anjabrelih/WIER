import sqlite3
import os
import nltk
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from stopwords import stop_words_slovene

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


# create db in folder implementation-indexing
if os.path.isfile("inverted-index.db"):
    conn = sqlite3.connect("inverted-index.db")
else:
    conn = sqlite3.connect("inverted-index.db")

    # Create table
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IndexWord (
        word TEXT PRIMARY KEY
        );
    ''')

    c.execute('''
        CREATE TABLE Posting (
            word TEXT NOT NULL,
            documentName TEXT NOT NULL,
            frequency INTEGER NOT NULL,
            indexes TEXT NOT NULL,
            PRIMARY KEY(word, documentName),
            FOREIGN KEY (word) REFERENCES IndexWord(word)
        );
    ''')

    # Save (commit) the changes
    conn.commit()

# Inserti word & | info into db
def insert_data(word, doc, freq, index):
    c = conn.cursor()
    
    # Insert word into db
    try:
        sql = "INSERT INTO IndexWord VALUES (?)"
        c.execute(sql, (word,))
        #print("last word id: ",c.lastrowid)

        # Save (commit) the changes
        conn.commit()
    except Exception as e:
        print("Word already exists in db", e)

    # Insert info into db (no need for try method)
    sql = "INSERT INTO Posting VALUES (?,?,?,?)"
    c.execute(sql, (word, doc, freq, index,))
    #print("last info id: ",c.lastrowid)

    # Save (commit) the changes
    conn.commit()
    

# Index words in html file
def index_words(html, doc):


    # Tokenize html file (and set it to lowercase)
    tokens = nltk.word_tokenize(html.text.lower())
    #print(tokens)
    #print(len(tokens))
    #print ("END of uncleaned tokens ------------")
    
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
        insert_data(t, doc, freq, str(index))
    
        
# Iterate over folders in input-indexing
input_indexing = ["../input-indexing/e-prostor.gov.si","../input-indexing/e-uprava.gov.si","../input-indexing/evem.gov.si","../input-indexing/podatki.gov.si"]
for folder in input_indexing:
    # read each file
    for file in os.listdir(folder):
        if file.endswith(".html"):
            path = os.path.join(folder,file)
            file_r = open(path, 'r', encoding="utf8")
            html = BeautifulSoup(file_r.read(), 'lxml')

            index_words(html, file)


# End - close the connection
conn.close()