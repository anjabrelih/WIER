import re
import json


def regex_rtvslo(html_content):
    # author, publishedTime, title, subtitle, lead, content
    output = {}
    
    # Regular expressions
    title = r'<h1>([^<]+)<\/h1>'
    subtitle = r'<div class="subtitle">([^<]+)<\/div>'
    author = r'<div class="author-timestamp">+[ \t\n]+<strong>([^<]+)<\/strong>'
    publishedTime = r'<div class="author-timestamp">+[ \t\n]+<strong>.*<\/strong>([^<]+)<\/div>'
    lead = r'<p class="lead">([^<]+)<\/p>'
    content = r'<\/div>[\s]*?<\/figure>[\s]*?<p([\s\S]*?)<div class=\"gallery\">'

    # Find    
    title = re.findall(title, html_content)
    subtitle = re.findall(subtitle, html_content)
    author = re.findall(author, html_content)
    publishedTime = re.findall(publishedTime, html_content)
    lead = re.findall(lead, html_content)
    content = re.findall(content, html_content)

    
    # Clean published time
    publishedTime = ' '.join(map(str,publishedTime)).strip('| ').replace("\n", "").replace("\t", "")

    # Clean lead
    lead = ' '.join(map(str, lead)).replace("\n","")
    if lead.endswith(" "):
        lead = lead[:-1]
    lead = " ".join(lead.split())

    # Clean content
    content = ' '.join(map(str,content)).replace("\n", "").replace("\t", "")
    content = re.findall(">([^<]+)", content)
    content = ' '.join(map(str,content))
    content = " ".join(content.split())


    # Output
    output = {
        "title": ", ".join(title),
        "subtitle": ", ".join(subtitle),
        "author": ", ".join(author),
        "published time": publishedTime,
        "lead": lead,
        "content": content
    }

    print(json.dumps(output, indent=3,separators=(',',':'), ensure_ascii=False))

    # Store to json file
    #out_file = open("../outputs/regex/rtvslo2.json", "w", encoding='utf8')
    #json.dump(output, out_file, indent=3,separators=(', ', ' : '), sort_keys=False, ensure_ascii=False)
    #out_file.close()

def regex_overstock(html_content):
    # title, listPrice, price, saving, savingPercent, content
    output = []

    # Regular expressions
    title = r'<b>(.+-[kK]t[^<]+)<\/b>'
    listPrice = r'List Price:</b></td><td align="left" nowrap="nowrap"><s>([^<]+)<\/s>'
    price = r'Price:</b></td><td align="left" nowrap="nowrap"><span class="bigred"><b>([^<]+)<\/b>'
    saving_both = r'You Save:</b></td><td align="left" nowrap="nowrap"><span class="littleorange">([^<]+)<\/span>'
    content = r'<span class=\"normal\">([^<]+)'


    # Find
    titles = re.findall(title, html_content)
    listPrices  = re.findall(listPrice , html_content)
    prices = re.findall(price, html_content)
    saving_boths = re.findall(saving_both, html_content) #clean
    contents = re.findall(content, html_content) #clean

    # Create strings and clean
    title_out = []
    for title in titles:
        title = ''.join(map(str, title))
        title_out.append(title)

    listPrice_out = []
    for listPrice in listPrices:
        listPrice = ''.join(map(str, listPrice))
        listPrice_out.append(listPrice)

    price_out= []
    for price in prices:
        price = ''.join(map(str, price))
        price_out.append(price)

    saving_out = []
    savingPercent_out = []
    for saving_both in saving_boths:
        saving_both=''.join(map(str,saving_both))
        saving = saving_both.split()
        saving_out.append(saving[0])
        savingPercent_out.append(saving[1].strip("()"))
    
    content_out = []
    for content in contents:
        content = ''.join(map(str,content))
        content_out.append(content.replace("\n"," "))    


    # Group
    for i in range(len(title_out)):
        item = {
            "title": title_out[i],
            "list price": listPrice_out[i],
            "price": price_out[i],
            "saving": saving_out[i],
            "saving percent": savingPercent_out[i],
            "content": content_out[i]
        }

        output.append(item)

    print(json.dumps(output, indent=3,separators=(',',':'), ensure_ascii=False))

    # Store to json file
    #out_file = open("../outputs/regex/overstock2.json", "w", encoding='utf8')
    #json.dump(output, out_file, indent=3,separators=(', ', ' : '), sort_keys=False, ensure_ascii=False)
    #out_file.close()


def regex_mimovrste(html_content):
    # title, price, available, number
    output = {}

    # Regular expressions
    title = r'<h1 data-v-8fdd7c3e="" class="detail__title detail__title--mobile">([^<]+)<\/h1>'
    price = r'<span class="price__wrap__box__final">([^<]+)<\/span>'
    available = r'<h3 class="availability-box__status availability-box__status--available">([^<]+)<\/h3>'
    number = r'class="detail-panel-under-title__text">([^<]+)<\/span>'

    # Find
    title = re.findall(title, html_content)
    price = re.findall(price,html_content)
    available = re.findall(available, html_content)
    number = re.findall(number, html_content)

    # Clean
    title = ' '.join(map(str,title)).replace("\n", "").replace("  ", "")
    available = ' '.join(map(str, available)).replace("\n", "").replace("  ", "")
    number = ' '.join(map(str,number)).replace("\n", "").replace("  ", "")
    number = number.split(': ')

    
    # Output
    output = {
        "title": title,
        "price": ", ".join(price),
        "available": available,
        "number": number[1]
    }

    print(json.dumps(output, indent=3,separators=(',',':'), ensure_ascii=False))

    # Store to json file
    #out_file = open("../outputs/regex/mimovrste2.json", "w", encoding='utf8')
    #json.dump(output, out_file, indent=3,separators=(', ', ' : '), sort_keys=False, ensure_ascii=False)
    #out_file.close()