import sqlite3
import time
import sys


def sqlite_search(query):

    conn = sqlite3.connect('inverted-index.db')
    c = conn.cursor()

    # Fix sql query, handle multime words
    cursor = c.execute('''
        SELECT p.documentName AS docName, SUM(frequency) AS freq, GROUP_CONCAT(indexes) AS idxs
        FROM Posting p
        WHERE
            p.word IN ('Tuš', 'Mercator')
        GROUP BY p.documentName
        ORDER BY freq DESC;
    ''')

    output = cursor

    # End - close connection to db
    conn.close()

    return output

if __name__ == '__main__':
    query = sys.argv[1]

    # !! handle multiple words

    # sqlite search
    start_time = time.time()
    output = sqlite_search(query)
    search_time = time.time() - start_time

    # rabis 5 zadetkov, 6 snippetov (če obstajajo?)
    for row in output:
        print(f"\tHits: {row[1]}\n\t\tDoc: '{row[0]}'\n\t\tIndexes: {row[2]}")


