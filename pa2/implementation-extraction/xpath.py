from numpy import number
from lxml import etree
import json


def xpath_rtvslo(html_content):
    # author, publishedTime, title, subtitle, lead, content
    output = {}

    html_doc = etree.HTML(html_content)

    # Find by XPath
    title = html_doc.xpath('//*[@id="main-container"]/div[3]/div/header/h1/text()')
    subtitle = html_doc.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]/text()')
    author = html_doc.xpath('//*[@id="main-container"]/div[3]/div/header/div[3]/div[1]/strong/text()')
    publishedTime = html_doc.xpath('//*[@id="main-container"]/div[3]/div/header/div[3]/div[1]/text()')
    lead = html_doc.xpath('//*[@class="lead"]/text()')
    content = html_doc.xpath('//*[@class="article-body"]/article/p/text()|//*[@class="article-body"]/article/p/strong/text()')

    # Clean
    publishedTime = ''.join(map(str,publishedTime[1])).strip('| ').replace("\n", "").replace("\t", "")
    
    lead = ' '.join(map(str, lead)).replace("\n","")
    if lead.endswith(" "):
        lead = lead[:-1]
    lead = " ".join(lead.split())

    content = ' '.join(map(str,content)).replace("\n", "").replace("\t", "")
    content = ' '.join(content.split())

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
    #out_file = open("../outputs/xpath/rtvslo2.json", "w", encoding='utf8')
    #json.dump(output, out_file, indent=3,separators=(', ', ' : '), sort_keys=False, ensure_ascii=False)
    #out_file.close()


def xpath_overstock(html_content):
    # title, listPrice, price, saving, savingPercent, content
    output = []
    item = {}

    html_doc = etree.HTML(html_content)

    # Find by XPath
    titles = html_doc.xpath('//*/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a/b/text()')
    listPrices = html_doc.xpath('//*/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()')
    prices = html_doc.xpath('//*/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()')
    saving_boths = html_doc.xpath('//*/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()')
    contents = html_doc.xpath('//*/span[@class="normal"]/text()|//*/span[@class="normal"]/a/span/b/text()')

    # Clean
    savings = []
    savingPercents = []
    for saving_both in saving_boths:
        savings_, savingPercents_ = saving_both.split()
        savings.append(savings_)
        savingPercents.append(savingPercents_.strip("()"))

    content_out = []
    for content in contents:
        if content == ("Click here to purchase."):
            continue
        else:
            if content.endswith(" "):
                content = content[:-1]
            content_out.append(content.replace("\n"," "))


    # Output
    for i in range(len(titles)):
        item = {
            "title": titles[i],
            "list price": listPrices[i],
            "price": prices[i],
            "saving": savings[i],
            "saving percent": savingPercents[i],
            "content": content_out[i]
        }

        output.append(item)

    print(json.dumps(output, indent=3,separators=(',',':'), ensure_ascii=False))

    # Store to json file
    #out_file = open("../outputs/xpath/overstock2.json", "w", encoding='utf8')
    #json.dump(output, out_file, indent=3,separators=(', ', ' : '), sort_keys=False, ensure_ascii=False)
    #out_file.close()


def xpath_mimovrste(html_content):
    # title, price, available, number, content
    output = {}

    html_doc = etree.HTML(html_content)

    # Find by XPath
    title = html_doc.xpath('//*[@class="product-box-simple__body__title"]/text()') #vzam enga in clean
    price = html_doc.xpath('//*[@class="price__wrap__box__final"]/text()')
    available = html_doc.xpath('//*[@class="availability-box__status availability-box__status--available"]/text()')
    number = html_doc.xpath('//*[@data-sel="catalog-number"]/text()')
   

    # Clean
    title = ' '.join(title[0].split())
    available = ' '.join(available).replace("\n","").replace("  ", "")

    # Output
    output = {
        "title": title,
        "price": ", ".join(price),
        "available": available,
        "number": ", ".join(number),
    }

    print(json.dumps(output, indent=3,separators=(',',':'), ensure_ascii=False))

    # Store to json file
    #out_file = open("../outputs/xpath/mimovrste2.json", "w", encoding='utf8')
    #json.dump(output, out_file, indent=3,separators=(', ', ' : '), sort_keys=False, ensure_ascii=False)
    #out_file.close()
