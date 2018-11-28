from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

request= Request("https://movie.naver.com/movie/sdb/rank/rmovie.nhn")
response= urlopen(request)
html = response.read().decode('cp949')

#print(html)
bs = BeautifulSoup(html,'html.parser')
# prettify = html 이쁘게 쓰기
# print(bs.prettify())

# find 만쓰면 처음거 하나만 가져오고 findAll쓰면 모두 가져온다
# html에서 div에서부터 class=tit3을 찾는다.
tags=bs.findAll('div', attrs={'class': 'tit3'})
#index = 0;

for index, tag in enumerate(tags):
   # index = index + 1
    print(index, tag.a['title'], tag.a['href'], sep=' - ')
