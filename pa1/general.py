import os

#Each website you crawl is a separate project (folder)

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


#Create queue and crawled files (if not created)

def create_data_files(project_name, base_url):
    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name,"crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url) #Base url is the first line
    if not os.path.isfile(crawled):
        write_file(crawled, '') #Crawled list is empty

#Create a new file
def write_file(path, data):
    with open(path, 'w') as f: #W for writting
        f.write(data)


#Create file queue.txt and crawled.txt in folder Dateoteke
#create_data_files('Datoteke','https://www.gov.si/')


#Add data onto an exisitng file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


#Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


#Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f: #read-text mode
        for line in f: #gre čez vse vrtice
            results.add(line.replace('\n', '')) #izbriše presledke
    return results        


#Iterate through a set, each item will be a new line in the file -> nasprotna operacija prejšne funkcije
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")
























