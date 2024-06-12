from bs4 import BeautifulSoup
import requests, re, smtplib, datetime, os,json
"""
scrape url and return results
"""
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

#lists to return at the end
previews = []
urls = []
headline_info = []

"""
look for image link, title, title link and add it to lists
"""
def getGoods(tags,img_class,title_element, title_class, switch,desc = None):
    for tag in tags:
 
        image = tag.find('div',class_=img_class)
        image = str(image.find('img')['src'])
        title = tag.find(title_element,class_=title_class)
        subtitle = ''

        #this is for allsides
        if switch == 1:
            urls.append('https://www.allsides.com'+str(title['href']))
        #intercept
        else:
            urls.append(str(tag['href']))
        title = title.getText()
        if desc:
            subtitle = tag.find('div',class_='headline-roundup-description').getText()

            article_preview = {
                'title': str(title),
               'subtitle': str(subtitle),
                'image': str(image)
            }
            headline_info.append(article_preview)
            return
        #print(title,subtitle,image)
        article_preview = {
            'title': str(title),
           'subtitle': str(subtitle),
            'image': str(image)
        }

        previews.append(article_preview)
"""
function to scrape a news website and return a bs4 result set based on a tag and class
link, tag, and class are all str type
"""
def webscrapeNews(link,tag,classs):        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        #website of choice
        read_news = scrapin(link,headers)
        find_elements = read_news.find_all(tag,class_=classs)
        return find_elements


def main():
    #news for allsides
    main_element = webscrapeNews(
                'https://www.allsides.com',
                'div',
                'headline-roundup large-roundup card-link'         
            )
    body_elements = webscrapeNews(
                'https://www.allsides.com',
                'div',
                'headline-roundup medium-roundup card-link'
            )
    # #news for intercept
    # intercept_elements = webscrapeNews(
    #             'https://theintercept.com/',
    #             'a',
    #             'content-card__link'
    #         )
    # #shorten intercept down to only two stories
    # intercept_elements = intercept_elements[:2]

    #retrieve information from elements and add it to lists
    getGoods(
                main_element, 
                'headline-roundup-image responsiveimg', 
                'a',
                'main-link',
                1, 
                True
            )
    getGoods(
                body_elements, 
                'headline-roundup-image responsiveimg', 
                'a',
                'main-link',
                1
            )
    # getGoods(
    #             intercept_elements, 
    #             'content-card__image', 
    #             'h3',
    #             'content-card__title',
    #             2
    #         )
    return previews, urls, headline_info
    