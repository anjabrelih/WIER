import sqlite3
import time
import sys
from bs4 import BeautifulSoup
import os
import nltk

from stopwords import stop_words_slovene


NO_SNIPPETS = 2
NO_RESULTS = 4


folder = "../input-indexing/"


def sqlite_search(query):

    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()

    # sql query for n number of words in query
    sql = sql = '''    
        SELECT p.word AS word, p.documentName AS docName, SUM(frequency) AS freq, GROUP_CONCAT(indexes) AS idxs
        FROM Posting p
        WHERE
            p.word IN ({seq})
        GROUP BY p.documentName
        ORDER BY freq DESC;'''.format(seq=','.join(['?']*len(query)))
    cursor = c.execute(sql, query)

    result = cursor.fetchall()
    n_results = len(list(result))

    # End - close connection to db
    conn.close()

    return result, n_results

def format_output(data, query):

    snippets = []
    doc = []

    # Format 6 snippets for 5 results
    for i, row in enumerate(data):
        # Correct document names (add folder - i didn't store this in db)
        if row[1].startswith("e-prostor"):
            document = "e-prostor.gov.si/"+row[1]
        if row[1].startswith("e-uprava"):
            document = "e-uprava.gov.si/"+row[1]
        if row[1].startswith("evem"):
            document = "evem.gov.si/"+row[1]
        if row[1].startswith("podatki"):
            document = "podatki.gov.si/"+row[1]
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
        query.append(q.lower())

    # sqlite search
    output, n_results = sqlite_search(query)

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
 
        print("\t{}".format(row[2]),"\t\t{}".format(doc[i]),"\t\t{}".format(snippets[i]))
        
        # Print only top n results
        if i == NO_RESULTS:
            break
