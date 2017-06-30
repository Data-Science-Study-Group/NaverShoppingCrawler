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
V 1.0


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

def getName(goods):
    name = (goods.find_all("a", class_="tit"))[0].contents[0]
    name = preProcessing(name)
    return name;

def getPrice(goods):
    # price have two kind
    try:
        price = (goods.find_all("span", class_="num _price_reload"))[0].text
    except:
        price = (goods.find_all("span", class_="num"))[0].text
    return price

def getSeller(goods):
    # seller have three kind
    try:
        seller = (goods.find_all("a", class_="mall_img"))[0].contents[0]
        seller = preProcessing(seller)
    except:
        sellertest = goods.find_all("p", class_="mall_txt")
        seller = (goods.find_all("p", class_="mall_txt"))[0].contents[1].text
        seller = preProcessing(seller)

        if seller == "":
            seller = sellertest[0].contents[1].contents[0].attrs["alt"]
    return seller

def main():
    print("""
    Naver Shopping Crawler (V1.0)
    Developed by StackCat
    """)
    while True:
        keyword = input("Input Keyword (--quit : exit) :")
        # url encode
        fnm = keyword
        keyword.replace(" ","+")
        keyword = parse.quote(keyword)

        if keyword =="--quit": exit()
        with open(fnm + '.json', 'w', encoding='utf8') as f:
            result = []
            for pagingIndex in range(1,11):
                # ban 방지용
                waitTime = random.randint(3,7)
                print("keyword:"+fnm+" | pagingIndex : "+str(pagingIndex) + " | wait : "+str(waitTime))

                url = "http://shopping.naver.com/search/all.nhn?query=" + keyword + "&pagingIndex="+str(pagingIndex)+"&pagingSize=80&viewType=list&sort=rel&frm=NVSHATC"
                bs = BeautifulSoup(urllib.request.urlopen(url),"html.parser")

                goods_list_result = bs.findAll("ul", class_="goods_list")
                i =0

                for ultag in goods_list_result:
                    for goods in ultag.contents:
                        if goods == "\n" : continue
                        try:
                            name = getName(goods)
                            price = getPrice(goods)
                            seller = getSeller(goods)

                        except:
                                print("\n\nerror\n\n\n{}\n\n\nerror\n\n".format(goods))
                                continue
                        data = { 'name':parse.unquote(name), 'price':parse.unquote(price), 'seller':parse.unquote(seller) }
                        result.append(data)
                if len(result) == 0 :
                    print("검색결과가 없습니다.")
                    break
                # ban 방지용
                sleep(waitTime)
            finalData = { 'size' : len(result), 'result': result }
            json.dump(finalData,f, ensure_ascii=False)

if __name__ == "__main__":
    main()
