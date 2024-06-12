from bs4 import BeautifulSoup
import requests, re, smtplib, datetime, os,json
def scrapin(url,user):
 
    res = requests.get(url,headers = user)
 
    res.status_code == requests.codes.ok
    #USED TO HALT A BAD DOWNLOAD
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    res_web = BeautifulSoup(res.text,'html.parser')
    return res_web
previews = []
urls = []
headline_info = []
def getGoods(tags,img_class,desc = None):
    for tag in tags:
 
        image = tag.find('div',class_=img_class)
        image = str(image.find('img')['src'])
        title = tag.find('a',class_='main-link')
        #link = str(title['href'])
        link = ''
        urls.append('https://www.allsides.com'+str(title['href']))

        title = title.getText()
        if desc:
            link = tag.find('div',class_='headline-roundup-description').getText()

            article_preview = {
                'title': str(title),
               'subtitle': str(link),
                'image': str(image)
            }
            headline_info.append(article_preview)
            return
        article_preview = {
            'title': str(title),
           'subtitle': str(link),
            'image': str(image)
        }

        previews.append(article_preview)
def webscrapeNews():        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        #website of choise
        read_news = scrapin('https://www.allsides.com/',headers)
        bigpapa = read_news.find_all('div',class_="headline-roundup large-roundup card-link")
        papa = read_news.find_all('div',class_="headline-roundup medium-roundup card-link")

        
        
        getGoods(bigpapa,'headline-roundup-image responsiveimg','here')
        getGoods(papa,'headline-roundup-image responsiveimg')


def scrapeIntercept():
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        #website of choise
        read_news = scrapin('https://theintercept.com/',headers)
        find_large = read_news.find_all('a',class_="content-card__link")
        #print(find_large)
        for tag in find_large:
    
            image = tag.find('div',class_="content-card__image")
            image = str(image.find('img')['src'])
            title = tag.find('h3',class_='content-card__title')
            print(title.getText(),tag['href'],image)
scrapeIntercept()        