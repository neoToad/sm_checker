from bs4 import BeautifulSoup as BSHTML
from urllib.request import Request, urlopen


req = Request('https://www.thepaperstore.com/c/squishmallows', headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req)
soup = BSHTML(page, 'lxml')
images = soup.findAll('img')
for image in images:
    try:
        #print image source
        print("src: " + image['src'])
    except KeyError:
        pass

    try:
        #print image source
        print("alt: " + image['alt'])
    except KeyError:
        pass