import time
from datetime import datetime
from itertools import count
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlretrieve
from __test.collection.crawler import crawling
import pandas as pd

RESULT_DIRECTORY = "__result"


def crawling_pelicana():
    results = []

    #시작과 끝이 있으면 range, 없으면 count 쓴다.
    for page in count(start=1):
    #for page in range(1, 2):
        html = crawling('http://www.pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' %page)

        bs= BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        if len(tags_tr)==0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            #print("%s : %s" % (name, address))
            results.append((name, address))

    # store(저장) # name, address를 타이틀로 테이블 만들기
    table = pd.DataFrame(results, columns=['name', 'address'] )

    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_kyochon():
    results=[]
        # 시작과 끝이 있으면 range, 없으면 count 쓴다.

    for sido1 in range(1, 17):
        for sido2 in count(start=1):
            url = ('http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' %(sido1, sido2))
            html = crawling(url)

            if html is None:
                break

            bs= BeautifulSoup(html,"html.parser")
            tag_ul = bs.find('ul', attrs={'class': 'list'})

            for tag_a in tag_ul.findAll('a'):
                tag_dt = tag_a.find('dt')
                if tag_dt is None :
                    break
                # text를 함수를 쓰고싶으면 겟_text() 파이썬에서는 언더바 자바는 getText()
                name = tag_dt.get_text()
                address = tag_a.find('dd').get_text().strip().split('\r\n')[0]
                # ---이거는 뒤에 스페이스가 있을수있으니 확인작업한것이다.
                #print("-------"+address+"--------")
                results.append((name, address))

    # store
    table = pd.DataFrame(results, columns=['name', 'address'] )
    table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_cheogajip():
    results=[]

    #for page in count(start=1):
    for page in range(103, 106):
        html=crawling("http://www.cheogajip.co.kr/bbs/board.php?bo_table=store&page=%d" %page)

        bs = BeautifulSoup(html, 'html.parser')
        tag_div = bs.find('div', attrs={"class": "tbl_head01"})
        tag_tbody = tag_div.find('tbody')
        tag_tr = tag_tbody.find('tr')
        tags_tr = tag_tbody.findAll('tr')
        tags_td = tag_tr.findAll('td')
        #print(tags_td)
        print(tags_tr)
        if tags_tr.findAll('td')[0].get('colspan') is not None:
            print("없다")
            break


        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[3]
            address = strings[5]
            results.append((name, address))

    table = pd.DataFrame(results, columns=['name', 'address'])
    table.to_csv('{0}/cheogajip_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_cheogajip1():
    results=[]

    #for page in count(start=1):
    for page in range(103, 106):
        html=crawling("http://www.cheogajip.co.kr/bbs/board.php?bo_table=store&page=%d" %page)

        bs = BeautifulSoup(html, 'html.parser')
        tag_div = bs.find('div', attrs={"class": "tbl_head01"})
        tag_tbody = tag_div.find('tbody')
        tags_tr = tag_tbody.findAll('tr')
        tags_tr2 = tag_tbody.find('tr')
        tags_td = tags_tr2.findAll('td')
        print(tags_td)
        if tags_td[0].get('colspan') is not None:
            print("없다")
            break


        for tag_tr in tags_tr:
            # tag_tr.strings만 프린트하면 주소값이 나온다. 스트링은 태그를 없애고 문자열을 출력한다.
            strings = list(tag_tr.strings)

            name = strings[3]
            address = strings[5]
            results.append((name, address))

    table = pd.DataFrame(results, columns=['name', 'address'])
    table.to_csv('{0}/cheogajip_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_goobne():
    url = "https://www.goobne.co.kr/store/search_store.jsp"

    #첫페이지 로딩
    wd = webdriver.Chrome('D:/Iot2018/chromedriver_win32/chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    results = []
    #for page in range(103, 104):
    for page in count(start=1):
        # 자바스크립트 실행
        script = 'store.getList(%d)' %page
        wd.execute_script(script)
        print('%s : success for request [%s]' % (datetime.now(), script))
        time.sleep(2)

        # 자바스크립트 실행 결과 HTML(렌더링된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id':'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            # string은 태그 다없애고 스트링으로
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]

            results.append((name, address))
            # store
            table = pd.DataFrame(results, columns=['name', 'address'])
            table.to_csv('{0}/goobne_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_nene():
    results=[]
    # 시작과 끝이 있으면 range, 없으면 count 쓴다.
    for page in count(start=1):
     # for page in range(49, 50):
        html = crawling('https://nenechicken.com/17_new/sub_shop01.asp?page=%d&ex_select=1&ex_select2=&IndexSword=&GUBUN=A' %page)
        bs = BeautifulSoup(html, 'html.parser')
        tags_div = bs.findAll('div', attrs={'class':'shopInfo'})


        for tag_div in tags_div:
            name = tag_div.find('div', attrs={'class': 'shopName'}).text
            address = tag_div.find('div', attrs={'class': 'shopAdd'}).text
            print("name : {}    address : {}".format(name,address))
            results.append((name, address))

        if len(tags_div) < 24:
            break

        # store(저장) # name, address를 타이틀로 테이블 만들기


def crawling_recipelist():
    results = []
    html = crawling('http://www.10000recipe.com/recipe/list.html?q=%EB%8B%AD%EB%B3%B6%EC%9D%8C%ED%83%95&order=accuracy&page=1')
    bs = BeautifulSoup(html, 'html.parser')
    tags_div = bs.findAll('div', attrs={'class':'col-xs-4'})

    print(len(tags_div))

    for tag_div in tags_div:
        title = tag_div.find('h4', attrs={'class':'ellipsis_title2'}).text
        results.append(title)
        print(title)
        if len(results) == 18:
            break

    table = pd.DataFrame(results, columns=['title'])
    table.to_csv('{0}/recipe_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_ingredient():
    results = []
    titles = []

    html = crawling("http://www.10000recipe.com/recipe/6887142")
    bs = BeautifulSoup(html, "html.parser")
    tag_div = bs.find("div", attrs={'class':'ready_ingre3'})

    tags_b = tag_div.findAll('b', attrs={'class':'ready_ingre3_tt'})
    for tag_b in tags_b:
        titles.append(tag_b.text)

    tags_li = tag_div.findAll('li')
    tags_span = tag_div.findAll('span', attrs={'class':'ingre_unit'})
    for i in range(0, len(tags_li)):
        ingredient = list(tags_li[i].strings)
        quantity = tags_span[i].text
        results.append((ingredient[0].strip(), quantity))
        # print((ingredient[0].strip(), quantity))



    table = pd.DataFrame(results, columns=[titles[0], titles[1]])
    table.to_csv('{0}/ingredient_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_recipe():
    results = []
    index = 1

    html = crawling('http://www.10000recipe.com/recipe/6887142')
    bs = BeautifulSoup(html, 'html.parser')

    while(True):
        tag_div = bs.find('div', attrs={'class': 'media-body', 'id': 'stepdescr' + str(index)})
        if tag_div == None:
            break
        results.append(tag_div.text)
        index += 1

    table = pd.DataFrame(results, columns=['과정'])
    table.to_csv('{0}/realrecipe_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_image():

    html = crawling('http://www.10000recipe.com/recipe/6887142')
    bs = BeautifulSoup(html, 'html.parser')

    tag_div = bs.find('div', attrs={'id':'stepimg1'})
    tag_img = tag_div.find('img')
    img_src = tag_img.get('src')
    print(img_src)
    img_url = img_src
    urlretrieve(img_src, 'test_img.jpg')



if (__name__=='__main__'):

    crawling_recipelist()
    crawling_recipe()
    crawling_ingredient()
    # crawling_image()



    # # pelicana
    # crawling_pelicana()
    #
    # # nene
    # crawling_nene()
    #
    # # kyochon
    # crawling_kyochon()
    #
    # # goobne
    # crawling_goobne()
    #
    # # cheogajip
    # crawling_cheogajip1()