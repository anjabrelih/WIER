import os
#from numpy import append

# Each website you crawl is a separate project (folder) - zbriši, ne rabimo te mape

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


#Create queue and crawled files (if not created) - zbriši, ne rabimo; moreš pa bazico uredit ane!

def create_data_files(project_name, base_url1):
    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name,"crawled.txt")
    Domains = os.path.join(project_name,"DOMAIN.txt")
    if not os.path.isfile(queue):
         write_file(queue, base_url1) #Base url is the first line
    if not os.path.isfile(crawled):
        write_file(crawled, '') #Crawled list is empty
    if not os.path.isfile(Domains):
        write_file(Domains, '') #IP list is empty


#Create a new file - zbriši, to je sam za kreirat datoteke
def write_file(path, data):
    with open(path, 'w') as f: #W for writting
        f.write(data)


#Create file queue.txt and crawled.txt in folder Dateoteke
#create_data_files('Datoteke','https://www.gov.si/')


#Add data onto an exisitng file -- zbriši, tukej (oziroma kr z db.py povežeš) dodaš povezave z bazo.
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


#Delete the contents of a file
#def delete_file_contents(path):
#    open(path, 'w').close()


# briši
#Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f: #read-text mode
        for line in f: #gre čez vse vrtice
            results.add(line.replace('\n', '')) #izbriše presledke
    return results        


# briši
#Iterate through a set, each item will be a new line in the file -> nasprotna operacija prejšne funkcije
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")

# briši
#READ TXT
def read_txt(path):
    file = open(path)
    return file





















