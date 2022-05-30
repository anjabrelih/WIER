from html.parser import HTMLParser
import os
import re
import sys
sys.setrecursionlimit(2000)

tokens = []

class RR_HTMLParse(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str]]) -> None:
        #return super().handle_starttag(tag, attrs)
        tokens.append(["starttag",tag, attrs])
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


def startRR(rtvslo1,rtvslo2,overstock1,overstock2,mimovrste1,mimovrste2,test1,test2):

    # User input for type of pages:
    user_input = input("Type 1 for rtvslo; 2 for overstock, 3 for mimovrste or 4 for test: ")

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
    elif user_input == "4":
        #print("You chose test.")
        page1 = test1
        page2 = test2
        name = "test"
    else:
        print("Parameter you entered is invalid. Run the code again.")


    # Clean pages
    page1 = clean_page(page1)
    page2 = clean_page(page2)
    #print("---------------")
    #print(page1)
    #print("---------------")
    #print("---------------")
    #print(page2)
    #print("---------------")

    # Activate parser
    parser = RR_HTMLParse()

    # Get tokens
    parser.feed(page1)
    tokens1 = list(tokens)
    print("TOKENS 1: ",tokens1)
    tokens.clear()

    parser.feed(page2)
    tokens2 = list(tokens)
    print("TOKENS 2: ", tokens2)
    tokens.clear()

    #print(tokens1)
    #print(tokens2[1])

    # Start roadRunner
    wrapper = []
    wrapper = roadRunner(tokens1, tokens2, 0, 0, wrapper)
    #print(wrapper)

    # Create final wrapper
    final_wrapper = create_wrapper(wrapper)
    #print(final_wrapper)

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
    try:
        t1 = tokens1[w]
    except:
        t1 = tokens1[-1]
    try:
        t2 = tokens2[s]
    except:
        t2 = tokens2[-1]

    # Check for matching tokens
    if check_match(t1, t2):
        # Match
        wrapper.append(t1)
        #print("Found match")
        return roadRunner(tokens1, tokens2, w+1, s+1, wrapper)
    else:
        # Doesnt match
        if t1[0] == "data" and t2[0] == "data":
            # Content mismatch (#PCDATA)
            wrapper.append(["data","#PCDATA"])
            #print("Found #PCDATA")
            return roadRunner(tokens1, tokens2, w+1, s+1, wrapper)

        else:
            # Check for iterations
            iteration = True

            # former tokens
            f_t1 = tokens1[w-1]
            f_t2 = tokens2[s-1]

            # page 1
            if f_t1[0] == "endtag" and t1[0] == "starttag" and f_t1[1] == t1[1]:
                # Check for end of found iteration
                flag = False
                i = w

                #print("Found iteration 1")

                while i <= len(tokens1):
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
                            # Mark start and end of iteration (if ends with endtag)
                            if subwrapper[-1][-2] == "endtag":
                                subwrapper[0][0] = "it-start"
                                subwrapper[-1][-2] = "it-end"

                            # Append subwrapper
                            for sub in subwrapper:
                                #print(sub)
                                wrapper.append(sub)
                            return roadRunner(tokens1, tokens2, i+1, s, wrapper)
                    else:
                        iteration = False
                else:
                    iteration = False
            else:
                iteration = False

    #print(wrapper)

            # page 2
            if f_t2[0] == "endtag" and t2[0] == "starttag" and f_t2[1] == t2[1]:
                # Check for end of found iteration
                flag = False
                i = s

                #print("Found iteration 2")

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
                        #print(tokens2[j:s])
                        #print("ITERATION 1: ",iteration1)
                        iteration2 = tokens2[s:i+1]
                        #print(tokens2[s:i+1])
                        #print("ITERATION 2: ",iteration2)

                        # Subwrapper
                        subwrapper = roadRunner(iteration1,iteration2, 0, 0, [])
                        #print("SUBWRAP")
                        #print(subwrapper)

                        if subwrapper != []:
                            # Mark start and end of iteration (if ends with endtag)
                            if subwrapper[-1][-2] == "endtag":
                                subwrapper[0][0] = "it-start"
                                subwrapper[-1][-2] = "it-end"

                            # Append subwrapper
                            for sub in subwrapper:
                                #print(sub)
                                wrapper.append(sub)
                            return roadRunner(tokens1, tokens2, w, i+1, wrapper)
                    else:
                        iteration = False               
                else:
                    iteration = False
            else:
                iteration = False
            

            #check for optional items
            if iteration == False:

                if len(tokens1) < w+1:
                    t2[0] = "optional"
                    wrapper.append(t2)
                    return roadRunner(tokens1, tokens2, w, s+1, wrapper)
                elif len(tokens2) < s+1:
                    t1[0] = "optional"
                    wrapper.append(t1)
                    return roadRunner(tokens1, tokens2, w+1, s, wrapper)
                elif check_match(tokens1[w+1], t2):
                    #print("one match case 1")
                    t1[0] = "optional"
                    #t1[1] = " ".join(["( ", t1[1]," )?"])
                    wrapper.append(t1)
                    return roadRunner(tokens1, tokens2, w+1, s, wrapper)
                elif check_match(t1, tokens2[s+1]):
                    t2[0] = "optional"
                    #t2[1] = " ".join(["( ", t2[1]," )?"])
                    wrapper.append(t2)
                    return roadRunner(tokens1, tokens2, w, s+1, wrapper)
                elif t1[1] == "img" and tokens1[w+1][0] == "endtag":
                    # Image is separated to start and endtag
                    t1[0] = "optional"
                    wrapper.append(t1)
                    return roadRunner(tokens1, tokens2, w+2, s, wrapper)
                elif t2[1] == "img" and tokens2[s+1][0] == "endtag":
                    # Image is separated to start and endtag
                    t2[0] = "optional"
                    wrapper.append(t2)
                    return roadRunner(tokens1, tokens2, w, s+2, wrapper)
                else:
                    # Multiple optional lines
                    mismatch1 = t1
                    mismatch2 = t2
                    m_w = w+2
                    m_s = s+2
                    page1 = False
                    page2 = False

                    while m_w < len(tokens1):
                        if tokens1[m_w] == mismatch2:
                            page1 = True
                            break
                        m_w += 1

                    while m_s < len(tokens2):
                        if tokens2[m_s] == mismatch1:
                            page2 = True
                            break
                        m_s += 1

                    if page1 == True:
                        for t1 in range(w, m_w):
                            tokens1[t1][0] == "optional"
                            wrapper.append(tokens1[t1])
                            return roadRunner(tokens1, tokens2, m_w, s, wrapper)
                    elif page2 == True:
                        for t2 in range(s, m_s):
                            tokens2[t2][0] == "optional"
                            wrapper.append(tokens2[t2])
                            return roadRunner(tokens1, tokens2, w, m_s, wrapper)
                    else:
                        # both elements are optional?
                        t1[0] = "optional"
                        wrapper.append(t1)
                        t2[0] = "optional"
                        wrapper.append(t2)
                        return roadRunner(tokens1, tokens2, w+1, s+1, wrapper)


                    
    return wrapper


    

def check_match(t1,t2):
    if t1[0] == t2[0] and t1[1] == t2[1]:
        if t1[0] == "starttag":
        # check if attributes match
            if t1[2] == t2[2]:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def clean_page(page):
    # Get rid of js and other nuisances :)
    #cleaner = Cleaner()
    #cleaner.javascript = True # This is True because we want to activate the javascript filter
    #cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter
    #cleaner.kill_tags = ['a', 'style', 'script', 'head', 'img', 'iframe', 'nav', 'svg', 'figure', 'map']

    #page = cleaner.clean_html(page)

    # https://stackoverflow.com/questions/8554035/remove-all-javascript-tags-and-style-tags-from-html-with-python-and-the-lxml-mod
    clean_script = r'<[ ]*script.*?\/[ ]*script[ ]*>'
    page = re.sub(clean_script, '', page, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
    clean_style = r'<[ ]*style.*?\/[ ]*style[ ]*>'
    page = re.sub(clean_style, '', page, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
    clean_meta = r'<[ ]*meta.*?>'
    page = re.sub(clean_meta, '', page, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
    clean_comment = r'<[ ]*!--.*?--[ ]*>'
    page = re.sub(clean_comment, '', page, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
    clean_doctype = r'<[ ]*\![ ]*DOCTYPE.*?>'
    page = re.sub(clean_doctype, '', page, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    #print("CLEANER ----------------")
    #print(page)
    #print("END CLEANER ----------------")

    page = page.split()
    page = " ".join(page)

    #print(type(page))
    
    return page


def create_wrapper(wrapper):
    
    ufre = ""

    for token in wrapper:
        #print(token)
        if token[0] == "starttag":
            if token[2] == []:
                ufre += "".join(["<", token[1], ">\n"])
            else:
                print(token[2])
                # get attributes if exist
                attributes = ""
                for el in token[2]:
                    at = "".join([el[0], "=\"",el[1],"\""])
                    attributes += "".join([" ",at])
                ufre += "".join(["<", token[1], attributes,">\n"])
        elif token[0] == "endtag":
            ufre += "".join(["</", token[1],">\n"])
        elif token[0] == "it-start":
            # Iteration start
            try:
                # get attributes if exist
                attributes = ""
                for el in token[2]:
                    at = "".join([el[0], "=\"",el[1],"\""])
                    attributes += "".join([" ",at])
                ufre += "".join(["(+ <", token[1], attributes,">\n"]) # Added + after ( bc there are multiple lines
            except:
                # no attributes
                ufre += "".join(["(+ <", token[1],">\n"])
        elif token[0] == "it-end":
            # Iteration end
            ufre += "".join(["<", token[1],"> )+\n"])
        elif token[0] == "optional":
            # Single optional item
            try:
                # get attributes if exist
                attributes = ""
                for el in token[2]:
                    at = "".join([el[0], "=\"",el[1],"\""])
                    attributes += "".join([" ",at])
                ufre += "".join(["( <", token[1], attributes,"> )?\n"])
            except:
                # no attributes
                ufre += "".join(["( <", token[1],"> )?\n"])
        elif token[0] == "op_start":
            # Optional items - start
            try:
                # get attributes if exist
                attributes = ""
                for el in token[2]:
                    at = "".join([el[0], "=\"",el[1],"\""])
                    attributes += "".join([" ",at])
                ufre += "".join(["(? <", token[1], attributes,">\n"]) # Added ? after ( bc there are multiple lines
            except:
                # no attributes
                ufre += "".join(["(? <", token[1],">\n"])
        elif token[0] == "op_end":
            # Iteration end
            ufre += "".join(["<", token[1],"> )?\n"])
        else:
            # Data
            ufre += token[1]+"\n"
            
        #print(ufre)

    return ufre
