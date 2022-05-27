# WIER Programming assignment 3
**Indexing and querying**

## Project consists of:
- (A) data processing with indexing
- (B) data retrieval with inverted index
- (C) data retrieval without inverted index

## File structure:
**implementation-indexing:**
- indexing.py (data processing with indexing)
- run-sqlite-search.py (data retrieval with inverted index)
- run-basic-search.py (data retrieval without inverted index)
- inverted-index.db (SQLite database file generated from indexing.py)
- stopwords.py (list of Slovene stopwords)

**input-indexing:**\
contains html files for data processing and retrieval in four folders.
- e-prostor.gov.si
- e-uprava.gov.si
- evem.gov.si
- podatki.gov.si


## Required libraries:
```sh
sqlite3
nltk
bs4
lxml
```

## Instructions:


Run code inside **implemetaction-indexing** folder:
- (A) data processing with indexing:
```sh
python indexing.py
```
- (B) data retrieval with inverted index:
```sh
python run-sqlite-search.py [SEARCH PARAMETERS]
```
- (C) data retrieval without inverted index:
```sh
python run-basic-search.py [SEARCH PARAMETERS]
```




