import lxml
from lxml.html.clean import Cleaner
from html.parser import HTMLParser
import os

tokens = []

class RR_HTMLParse(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str]]) -> None:
        #return super().handle_starttag(tag, attrs)
        tokens.append(["starttag",tag])
        #print("starttag: ",tag)

    def handle_endtag(self, tag) -> None:
        #return super().handle_endtag(tag)
        tokens.append(["endtag",tag])
        #print("endtag: ",tag)

    def handle_data(self, data: str) -> None:
        #return super().handle_data(data)
        if data != ' ':
            tokens.append(["data", data])
            #print("data: ", data)


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


    # Clean pages
    page1 = clean_page(page1)
    page2 = clean_page(page2)
    print(page1)

    # Activate parser
    parser = RR_HTMLParse()

    # Get tokens
    parser.feed(page1)
    tokens1 = list(tokens)
    #print("TOKENS 1: ",tokens1)
    tokens.clear()

    parser.feed(page2)
    tokens2 = list(tokens)
    #print("TOKENS 2: ", tokens2)
    tokens.clear()

    #print(tokens1)
    #print(tokens2[1])

    # Start roadRunner
    wrapper = []
    wrapper = roadRunner(tokens1, tokens2, 0, 0, wrapper)
    #print(wrapper)

    # Create final wrapper
    final_wrapper = create_wrapper(wrapper)
    print(final_wrapper)

    # Store to html file
    file = "../outputs/roadRunner/"+name+"_wrapper.html"
    os.makedirs(os.path.dirname(file), exist_ok=True)
    out_file = open(file, "w", encoding='utf8')
    out_file.write(final_wrapper)
    out_file.close()

    

def roadRunner(tokens1, tokens2, w, s, wrapper):

    # No new tokens to compare
    if w == len(tokens1) and s == len(tokens2):
        return wrapper

    t1 = tokens1[w]
    t2 = tokens2[s]

    # Check for matching tokens
    if check_match(t1, t2):
        # Match
        wrapper.append(t1)
        return roadRunner(tokens1, tokens2, w+1, s+1, wrapper)
    else:
        # Doesnt match
        if t1[0] == "data" and t2[0] == "data":
            # Content mismatch (#PCDATA)
            wrapper.append(["data","#PCDATA"])
            return roadRunner(tokens1, tokens2, w+1, s+1, wrapper)

        else:
            # Check for iterations
            iteration = True

            # former tokens
            f_t1 = tokens1[w-1]
            f_t2 = tokens2[s-1]

            # page 1
            if f_t1[0] == "endtag" and t1[0] == "starttag" and f_t1[0] == t1[0]:
                # Check for end of found iteration
                flag = False
                i = w

                while i < len(tokens1):
                    if tokens1[i][0] == "endtag" and tokens1[i][1] == tokens1[w][1]:
                        flag = True
                        #print("FOUND ITERATION 1 end")
                        break
                    i = i+1


                # When iteration end found
                if flag:
                    # Find start of first iteration (w-1)
                    flag = False
                    j = w-1

                    while j > 0:
                        if tokens1[j][0] == "starttag" and tokens1[j][1] == tokens1[w-1][1]:
                            flag = True
                            #print("FOUND ITERATION 1 start")
                            break
                        j = j-1

                    if flag:
                        # Create wrapper for iterations
                        iteration1 = tokens1[j:w]
                        #print("ITERATION 1: ",iteration1)
                        iteration2 = tokens1[w:i+1]
                        #print("ITERATION 2: ",iteration2)

                        # Subwrapper
                        subwrapper = roadRunner(iteration1,iteration2, 0, 0, [])

                        if subwrapper != []:
                            wrapper.append(subwrapper)
                            return roadRunner(tokens1, tokens2, i+1, s, wrapper)
                    else:
                        iteration = False
                else:
                    iteration = False
            else:
                iteration = False

    #print(wrapper)

            # page 2
            if f_t2[0] == "endtag" and t2[0] == "starttag" and f_t2[0] == t2[0]:
                # Check for end of found iteration
                flag = False
                i = s

                while i < len(tokens2):
                    if tokens2[i][0] == "endtag" and tokens2[i][1] == tokens2[s][1]:
                        flag = True
                        #print("FOUND ITERATION 2 end")
                        break
                    i = i+1


                # When iterations found
                if flag:
                    # Find start of first iteration (w-1)
                    flag = False
                    j = s-1

                    while j > 0:
                        if tokens2[j][0] == "starttag" and tokens2[j][1] == tokens2[s-1][1]:
                            flag = True
                            #print("FOUND ITERATION 2 start")
                            break
                        j = j-1

                    if flag:
                        # Create wrapper for iterations
                        iteration1 = tokens2[j:s]
                        #print("ITERATION 1: ",iteration1)
                        iteration2 = tokens2[s:i+1]
                        #print("ITERATION 2: ",iteration2)

                        # Subwrapper
                        subwrapper = roadRunner(iteration1,iteration2, 0, 0, [])

                        if subwrapper != []:
                            wrapper.append(subwrapper)
                            return roadRunner(tokens1, tokens2, w, i+1, wrapper)
                    else:
                        iteration = False               
                else:
                    iteration = False
            else:
                iteration = False


            #check for optional items
            if iteration == False:
                if check_match(tokens1[w+1], t2):
                    optional_item = ["optional", " ".join(["(", t1[1],")(optional?)"])]
                    wrapper.append(optional_item)
                    return roadRunner(tokens1, tokens2, w+1, s, wrapper)
                elif check_match(t1, tokens2[s+1]):
                    optional_item = ["optional", " ".join(["(", t2[1],")(optional?)"])]
                    wrapper.append(optional_item)
                    return roadRunner(tokens1, tokens2, w, s+1, wrapper)
                else:
                   return wrapper

    return wrapper
    
    

def check_match(t1,t2):
    if t1[0] == t2[0] and t1[1] == t2[1]:
        return True
    else:
        return False


def clean_page(page):
    # Get rid of js and other nuisances :)
    cleaner = Cleaner()
    cleaner.javascript = True # This is True because we want to activate the javascript filter
    cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter
    #cleaner.kill_tags = ['a', 'style', 'script', 'head', 'img', 'iframe', 'nav', 'svg', 'figure', 'map']

    page = cleaner.clean_html(page)

    page = page.split()
    page = " ".join(page)

    #print(type(page))
    
    return page


def create_wrapper(wrapper):
    
    ufre = ""

    for token in wrapper:
        if token[0] == "starttag":
            ufre += "".join(["<", token[1],">\n"])
        elif token[0] == "endtag":
            ufre += "".join(["</", token[1],">\n"]) 
        else:
            ufre += token[1]+"\n"

    return ufre
