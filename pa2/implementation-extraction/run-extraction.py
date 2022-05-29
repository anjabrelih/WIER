import codecs
import sys

import regex
import xpath
import roadRunner


# Get html files
rtvslo1 = codecs.open("../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", "r","utf-8").read()
rtvslo2 = codecs.open("../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html", "r","utf-8").read()

overstock1 = codecs.open("../input-extraction/overstock.com/jewelry01.html","r","ISO-8859-1").read()
overstock2 = codecs.open("../input-extraction/overstock.com/jewelry02.html","r","ISO-8859-1").read()

mimovrste1 = codecs.open("../input-extraction/mimovrste.com/Apple MacBook Pro prenosnik, 14.2, 512 GB, Space Grey (mkgp3cr_a) _ mimovrste=).html", "r","utf-8").read()
mimovrste2 = codecs.open("../input-extraction/mimovrste.com/Apple MacBook 13 Air prenosnik, 256 GB, Space Gray, SLO KB (MGN63CR_A) _ mimovrste=).html", "r","utf-8").read()

test1 = codecs.open("../input-extraction/test/test1.html", "r","utf-8").read()
test2 = codecs.open("../input-extraction/test/test2.html", "r","utf-8").read()

# User input - extraction method
def choose_extraction(input):

    if input == "A":
        print("Regex RTVSLO 1:")
        regex.regex_rtvslo(rtvslo1)
        print("Regex RTVSLO 2:")
        regex.regex_rtvslo(rtvslo2)

        print("Regex OVERSTOCK 1:")
        regex.regex_overstock(overstock1)
        print("Regex OVERSTOCK 2:")
        regex.regex_overstock(overstock2)

        print("Regex MIMOVRSTE 1:")
        regex.regex_mimovrste(mimovrste1)
        print("Regex MIMOVRSTE 2:")
        regex.regex_mimovrste(mimovrste2)

    elif input == "B":
        print("XPath RTVSLO 1:")
        xpath.xpath_rtvslo(rtvslo1)
        print("XPath RTVSLO 2:")
        xpath.xpath_rtvslo(rtvslo2)

        print("XPath OVERSTOCK 1:")
        xpath.xpath_overstock(overstock1)
        print("XPath OVERSTOCK 2:")
        xpath.xpath_overstock(overstock2)

        print("XPath MIMOVRSTE 1:")
        xpath.xpath_mimovrste(mimovrste1)
        print("XPath MIMOVRSTE 2:")
        xpath.xpath_mimovrste(mimovrste2)

    elif input == "C":
        roadRunner.startRR(rtvslo1,rtvslo2,overstock1,overstock2,mimovrste1,mimovrste2,test1,test2)

    else:
        print("Valid input parameters are A, B or C!")

if __name__ == "__main__":
    choose_extraction(sys.argv[1])
