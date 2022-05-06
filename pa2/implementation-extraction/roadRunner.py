import lxml
from lxml.html.clean import Cleaner
import bs4
import os
import copy


def startRR(rtvslo1,rtvslo2,overstock1,overstock2,mimovrste1,mimovrste2):

    # User input for type of pages:
    user_input = input("Type 1 for rtvslo; 2 for overstock or 3 for mimovrste: ")

    # Clean chosen pages
    if user_input == "1":
        #print("You chose rtvslo.")
        page1 = rtvslo1
        page2 = rtvslo2
        name = "rtvslo"
    elif user_input == "2":
        #print("You chose overstock.")
        page1 = overstock1
        page2 = overstock2
        name = "overstock"
    elif user_input == "3":
        #print("You chose mimovrste.")
        page1 = mimovrste1
        page2 = mimovrste2
        name = "mimovrste"
    else:
        print("Parameter you entered is invalid. Run the code again.")


    # Start Roadrunner with selected pages
    roadRunner(page1, page2, name)

    #print(clean_page(page1))
    # OUUUUUT store to html file
    #file = "../pa2/test_wrappers"+"rtvslo2"+"_wrapper.html"
    #os.makedirs(os.path.dirname(file), exist_ok=True)
    #out_file = open(file, "w", encoding='utf8')
    #out_file.write(clean_page(page2).prettify())
    #out_file.close()

    

def roadRunner(page1, page2, name):

    # Clean and convert to lxml
    bs_page1 = clean_page(page1)
    bs_page2 = clean_page(page2)

    # Create wrapper
    wrapper = create_wrapper(bs_page1, bs_page2)

    # Store to html file
    #file = "../outputs/roadRunner/"+name+"_wrapper.html"
    #os.makedirs(os.path.dirname(file), exist_ok=True)
    #out_file = open(file, "w", encoding='utf8')
    #out_file.write(wrapper.prettify())
    #out_file.close()


def clean_page(page):
    # Get rid of js and other nuisances :)
    cleaner = Cleaner()
    cleaner.javascript = True # This is True because we want to activate the javascript filter
    cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter
    cleaner.kill_tags = ['a', 'style', 'script', 'head', 'img', 'iframe', 'nav', 'svg', 'figure', 'map']

    page = cleaner.clean_html(page)

    page = bs4.BeautifulSoup(page, "lxml")

    # If some tag attributes (other than class and id) still remain
    for tag in page.find_all(True):
        class_attribute = None
        id_attribute = None

        if tag.has_attr('class'):
            class_attribute = tag['class']

        if tag.has_attr('id'):
            id_attribute = tag['id']

        tag.attrs = {}

        if class_attribute != None:
            tag.attrs['class'] = class_attribute
        if id_attribute != None:
            tag.attrs['id'] = id_attribute
  

    return page


def create_wrapper(page1, page2):
    
    matchingTag = 1 # True - is matching
    
    #Decouple pages
    elements1 = [copy.copy(el) for el in page1.children if not (isinstance(el, bs4.NavigableString) and el.string.isspace())]
    elements2 = [copy.copy(el) for el in page2.children if not (isinstance(el, bs4.NavigableString) and el.string.isspace())]


    #if len(elements1) == 0 and len(elements2) == 0:
        #return elements1

    
    i = 0
    # Go through all elements
    #while i < len(elements1) or i < len(elements2):

    #print(len(elements1))
    #for element in (page1.childern):
     #   print("bleh")
    #print(elements2[i])






    



    


