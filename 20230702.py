#%%

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page1.html")
bs=BeautifulSoup(html.read(), 'html.parser')
print(bs.h1)

#%%

html = urlopen("http://www.pythonscraping.com/pages/page1.html")
bs=BeautifulSoup(html, 'html.parser')
print(bs.h1)

#%%

# 페이지의 제목 가져오는 함수
# 서버 상태가 안좋을때 오류와 url 잘못 입력했을 때 
# 결과값을 none으로 통일, 오류나서 프로그램이 멈추진 않음

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.error import URLError

def getTitle(url):
    try:
        html=urlopen(url)
    except HTTPError as e:
        return None
    except URLError as e:
        return None
    try:
        bs=BeautifulSoup(html.read(), 'html.parser')
        title=bs.body.h1
    except AttributeError as e:
        return None
    return title

title=getTitle('http://www.pythonscracing.com/pages/page1.html')
if title==None:
    print("Title not found")
else:
    print(title)

#%%

# findAll 함수 : 태그의 이름과 속성을 이용해 
# 특정 종류의 태그를 찾아내고 ResultSet이라는 객체로 저장
# get_text로 객체 내 태그들의 텍스트만 추출(헤더, 태그 말고)

from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs=BeautifulSoup(html, 'html.parser')

namelist=bs.findAll('span', {'class':'green'})
for name in namelist:
    print(name.get_text())

#%%

# 2장. 고급 HTML 분석
# 트리 이동 - 자식과 자손

from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen('http://www.pythonscraping.com/pages/page3.html')
bs=BeautifulSoup(html, 'html.parser')

# 태그 종류: table, 'giftList'라는 이름을 가진 table 태그
# 이때 열 이름들도 다 가져옴 (첫 행을 실제 데이터 내용부터 시작 X)

for child in bs.find('table', {'id':'giftList'}).children:
    print(child)
    
#%%

from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen('http://www.pythonscraping.com/pages/page3.html')
bs=BeautifulSoup(html, 'html.parser')

# children과 descendent 의 차이??

for desc in bs.find('table', {'id':'giftList'}).descendants:
    print(desc)
    
#%%

from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen('http://www.pythonscraping.com/pages/page3.html')
bs=BeautifulSoup(html, 'html.parser')

# 선택된 첫 행 (tr) 이후의 자식의 형제들만 추출
# 따라서 선택된 첫 행인 열 이름은 포함되지 않음

for sib in bs.find('table', {'id':'giftList'}).tr.next_siblings:
    print(sib)
    
#%%

from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen('http://www.pythonscraping.com/pages/page3.html')
bs=BeautifulSoup(html, 'html.parser')
print(bs.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())

# 3장. 크롤링 시작하기
# 정규 표현식 이용해 재귀적 크롤링 해보기

#%%
from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
bs=BeautifulSoup(html, 'html.parser')
for link in bs.findAll('a'):
    if 'href' in link.attrs:
        print(link.attrs['href'])
        
#%%

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())

def getWikiLinks(articleUrl):
    html=urlopen('http://en.wikipedia.org{}'.format(articleUrl))
    bs=BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'id':'bodyContent'}).findAll('a',href=re.compile('^(/wiki/)((?!:).)*$'))

links=getWikiLinks('/wiki/Kevin_Bacon')
count=0
while len(links)>0:
    if count==10:
        break
    else:
        newArticle=links[random.randint(0,len(links)-1)].attrs['href']
        print(newArticle)
        links=getWikiLinks(newArticle)
        count+=1
        
