import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


baseurl = 'https://cafef.vn'
linklist = []

for x in range(1,2):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    url = f'https://cafef.vn/doc-nhanh/trang-{x}.chn'
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('div', class_='nv-text-cont')
        print(f'Getting link - trang {x}')
        for article in articles:
            link = baseurl + article.find('a')['href']
            linklist.append(link)
        print (len(linklist))
    except:
        print(f'Getting link - trang {x}' + ':FAIL - TIMEOUT' )
    time.sleep(3)

articleslist = []
linkfail = []
for item in linklist: 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    try:
        r = requests.get(item,headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('h1', class_='title').text.strip()
        source = soup.find('p', class_='source').text
        date = soup.find('span', class_='pdate').text[0:10]   #29-08-2022 - 14:14 PM
        menu = soup.find('a', class_='cat').text
       
        article = {
            'title': title,
            'menu': menu,
            'date': date,
            'link': item,
            'source': source                    
        }
        articleslist.append(article)
    except:
        print('Load page Fail: ' + item)
        linkfail.append(item)

df = pd.DataFrame(articleslist)
df.to_excel('Cafef_5000.xlsx', index=True)
df2 = pd.DataFrame(linkfail)
df2.to_excel('Cafef_FAIL.xlsx', index=True)
print('Total Articles:' + str(len(articleslist)) + '===' + 'TOTAL FAIL: ' + str(len(linkfail)))
print('Saved to CSV file.')


