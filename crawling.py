# -*-coding:utf-8-*-
import requests, re
from bs4 import BeautifulSoup
from urllib import parse
import json
import urllib
import random
from time import sleep

"""
2017. 06. 29 Developed by KYT
NaverShopping Crawler
V 1.13


class info--
img : div - img_area
name : div - info
price : span - num_price_reload
shop name : p - mall_txt > a 
other : depth, etc
"""

def preProcessing(str):
    result = re.sub("\n","", str)
    result = re.sub("\t","",result)
    return result

def getDisplayedName(goods):
    try:
        nameSet = goods.find_all("a", class_="tit")
        name = nameSet[0]['title']
        name = preProcessing(name)
    except:
        name = nameSet[0].contents[0]
    return name

def getName(goods):
    sleepTime = random.randint(3,7)
    displayedName = getDisplayedName(goods)
    metaURL = getMetaURL(goods, sleepTime)

    if metaURL.find("storefarm.naver.com") > 0 :
        #metaURL = metaURL.encode("utf-8")
        bsRealName = BeautifulSoup(urllib.request.urlopen(metaURL), "html.parser")
        realNameSet = bsRealName.find_all("dt", class_="prd_name")
        realName = realNameSet[0].text
        return realName
    else :
        return displayedName

def getMetaURL(goods, sleepTime=0):
    print("[getMetaURL] ip ban 방지를 위해 sleep합니다......({} sec)".format(sleepTime))
    sleep(sleepTime)
    href = (goods.find_all("a", class_="tit"))[0].attrs["href"]
    bsMeta = BeautifulSoup(urllib.request.urlopen(href), 'html.parser')
    meta = bsMeta.find("meta",property="og:url")

    #metaURL = meta["content"] if meta is not None else href
    if meta is not None:
        metaURL = meta["content"]
    else:
        metaURLSet = bsMeta.find_all("div", class_="naver-splugin")
        metaURL = href if len(metaURLSet) == 0 else metaURLSet[0]["data-url"]
    return metaURL

def getPrice(goods):
    # price have two kind
    try:
        priceSet = goods.find_all("span", class_="num _price_reload")
        price = priceSet[0].text
    except:
        try:
            priceSet = goods.find_all("span", class_="num")
            price = priceSet[0].text
        except:
            print("\n\nerror on getPrice\n\n\n{}\n\n\nerror\n\n".format(goods))
    return price

def getSeller(goods):
    # seller have three kind
    try:
        sellerSet = goods.find_all("a", class_="mall_img")
        seller = sellerSet[0].contents[0]
        seller = preProcessing(seller)
        if seller == '' :
            raise(AttributeError)
    except:
        try:
            sellerSet = goods.find_all("p", class_="mall_txt")
            seller = sellerSet[0].contents[1].text
            seller = preProcessing(seller)

            if seller == "":
                seller = goods.find_all("span", class_="mall_name")[0].text
        except:
            try:
                seller = sellerSet[0].contents[1].contents[0].attrs["alt"]
            except:
                print("\n\nerror on getSeller\n\n\n{}\n\n\nerror\n\n".format(goods))
    return seller

def getDeliveryPrice(goods):
    # DPrice have three kind  (someInt, free, null)
    try:
        DPriceSet = (goods.find_all("ul", class_="mall_option"))
        DPrice = DPriceSet[0].contents[1].text
        if "배송비" not in DPrice:
            DPrice = DPriceSet[0].contents[3].text

        DPrice = preProcessing(DPrice)
        DPrice = DPrice.replace("배송비 ","")
        DPrice = DPrice.replace("원", "")
    except:
        try:
            if len(DPriceSet) == 0 :
                DPrice = "정보없음"
        except:
            print("\n\nerror on getDeliveryPrice\n\n\n{}\n\n\nerror\n\n".format(goods))

    return DPrice

def main():
    print("""
    Naver Shopping Crawler (V1.13)
    Developed by StackCat
    """)
    keyword = input("Input Keyword (--quit : exit) :")
    maxPaging = input("Input maxPaging : ")
    # url encode
    fnm = keyword
    keyword.replace(" ","+")
    keyword = parse.quote(keyword)

    if keyword =="--quit": exit()
    with open(fnm + '.json', 'w', encoding='utf8') as f:
        result = []
        for pagingIndex in range(1,int(maxPaging)+1):

            # ban 방지용
            waitTime = random.randint(10,15)
            print("keyword:"+fnm+" | pagingIndex : "+str(pagingIndex) + " | wait : "+str(waitTime))

            url = "http://shopping.naver.com/search/all.nhn?query=" + keyword + "&pagingIndex="+str(pagingIndex)+"&pagingSize=80&viewType=list&sort=rel&frm=NVSHATC"
            bs = BeautifulSoup(urllib.request.urlopen(url),"html.parser")

            goods_list_result = bs.findAll("ul", class_="goods_list")
            i =0

            for ultag in goods_list_result:
                for goods in ultag.contents:
                    name = price = seller = DPrice = 0
                    data = {}
                    if goods == "\n" : continue
                    name = getName(goods)
                    price = getPrice(goods)
                    seller = getSeller(goods)
                    DPrice = getDeliveryPrice(goods)
                    data = { 'name':parse.unquote(name), 'price':parse.unquote(price), 'seller':parse.unquote(seller), 'DeliveryPrice':parse.unquote(DPrice) }
                    result.append(data)
            if len(data) == 0 :
                print("검색결과가 없습니다.")
                break

            # ban 방지용
            if pagingIndex % 11 == 0 :
                print("11페이지마다 조금 더 오래 쉽니다(25초, ban 방지용)")
                sleep(25)
            elif pagingIndex < maxPaging :
                sleep(waitTime)


        finalData = { 'size' : len(result), 'result': result }
        json.dump(finalData,f, ensure_ascii=False)

if __name__ == "__main__":
    main()
