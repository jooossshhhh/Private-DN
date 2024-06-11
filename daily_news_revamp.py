
from pprint import pprint
from bs4 import BeautifulSoup
import requests, re, smtplib, datetime, os,json

from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('API_KEY')
email = os.getenv('EMAIL')
passwd = os.getenv('PASSWORD')
WEATHER_API = os.getenv('WEATHER_API_KEY')

def email_alert(subject,body,alternative,recipients):
    for recipient in recipients:
 
        msg = EmailMessage()
        msg.set_content(body)
        if alternative:
            msg.add_alternative(alternative,'html')
        msg['subject'] = subject
        
        msg['to'] = recipient
        user = email
        password = passwd
        msg['from'] = 'First Sip'
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user,password)
        server.send_message(msg)
        server.quit()

def todaysDate():
    # Get today's date
    today = datetime.datetime.today()
    
    # Format the date
    formatted_date = today.strftime("%A, %B %d")
    
    # Add appropriate suffix to the day
    day_suffix = "th" if 11 <= today.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(today.day % 10, "th")
    
    # Concatenate the suffix to the formatted date
    formatted_date += day_suffix
    
    # return the formatted date
    return formatted_date
 
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
        mama = read_news.find_all('div',class_="headline-roundup small-roundup card-link")
        
        
        getGoods(bigpapa,'headline-roundup-image responsiveimg','here')
        getGoods(papa,'headline-roundup-image responsiveimg')
        #getGoods(mama,'headline-roundup-image')
def betterWeather(zipcode):
    base_url = "https://api.openweathermap.org"
    weather_api = WEATHER_API

    geoip = base_url+"/geo/1.0/zip?zip="+zipcode+"&appid="+weather_api
    georesponse = requests.get(geoip)
    x=georesponse.json()
    lat = x['lat']
    lng = x['lon']
    weather_url = base_url + "/data/2.5/weather?lat="+str(lat)+"&lon="+str(lng)+"&appid="+weather_api+"&units=imperial"
    response = requests.get(weather_url)
    y=response.json()
    #pprint(y)
    icon_image = "https://openweathermap.org/img/wn/" + y['weather'][0]['icon'] + "@2x.png"
    degree_sign = u'\N{DEGREE SIGN}'
    sunrise = datetime.datetime.fromtimestamp(y['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.datetime.fromtimestamp(y['sys']['sunset']).strftime('%H:%M')
    city = str(y['name'])
    highlow = 'High : ' + str(int(y['main']['temp_max']))+degree_sign + '<br>Low : ' +str(int(y['main']['temp_min']))+degree_sign
    sun = 'Sunrise : ' + str(sunrise) + '<br>Sunset : ' + str(sunset)
    humidity = 'Humidity : ' + str(y['main']['humidity']) + '%'

    weather_template = '<hr><h3>Weather for ' + city + '</h3><br><p ><table><tr><th>' + highlow  + '<br>' + sun + '<br>' + humidity + "</th><th style='padding-left:0.8em'><img src='" + icon_image +"'/></th></tr></table></p>"
    # weather_template = '<hr><h3>Weather for ' + city + '</h3><br><p >' + highlow  + '<br>' + sun + '<br>' + humidity + "</p>"
    return weather_template

def getWotd():
    
    #we are finding the word of the day - just scraping a website for it
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    read = scrapin('https://www.merriam-webster.com/word-of-the-day', headers)
    #wotd=read.find('div',class_='word-and-pronunciation')
    wotdef=read.find('div',class_='wod-definition-container')
    wotday = read.find('h2',class_='word-header-txt')
    #print(wotday.getText())
    wotdeff=str(wotdef)
    
    wotd_def = wotdeff[wotdeff.find('<p>')+3:wotdeff.find('</p>')]

    insensitive_wotd = re.compile(re.escape(wotday.getText()), re.IGNORECASE)
    wotd_linked = insensitive_wotd.sub('<a href=https://www.merriam-webster.com/word-of-the-day><em>'+wotday.getText()+'</em></a>', wotd_def)
    
    #print(wotd_linked)
    #return '<div><h3><b>Word of the day</h3>'+wotd_linked+'</div>'
    return '<hr><h3>Word of the Day</h3><br><p>' + wotd_linked +'</p>'
 
word = getWotd()

webscrapeNews()
template = open(r'email.html')
soup = BeautifulSoup(template.read(), "html.parser")
#word = BeautifulSoup(word, "html.parser")
article_template = soup.find('div', attrs={'class':'columns'})

headline = soup.find('div',attrs={'class':'headline'})
img = headline.img
img['src'] = headline_info[0]['image']
subtitle = headline.p
subtitle.string = headline_info[0]['subtitle'][:300] 
 
link = headline.a

link['href'] = urls[0]
urls.pop(0)
link.string = headline_info[0]['title'][:300]#urls[i]

html_start = str(soup)[:str(soup).find(str(article_template))]
#html_start.replace('src=""','src="'+headline_info[0]['image']+'"')

html_end = str(soup)[str(soup).find(str(article_template))+len(str(article_template)):]
 
html_start = html_start.replace('\n','')
html_end = html_end.replace('\n','')

newsletter_content = ""
for i,article in enumerate(previews):
    print(i)
    try:
        img = article_template.img
        #print(img)
        img['src'] = article['image']
        article_template.img.replace_with(img)
    except:
        pass

    subtitle = article_template.p
    subtitle.string = article['subtitle'][:300] 
 
    link = article_template.a

    link['href'] = urls[i]
    link.string = article['title'][:300]#urls[i]

    article_template.a.replace_with(link)
 
    newsletter_content += str(article_template).replace('\n','')


#email_content =  html_start +  newsletter_content + betterWeather('37122') + word + html_end
#email_content=email_content.replace('</table></div><div class="columns"><table>','')

def main():
    f = open('email_zip.json')
    data = json.load(f)
    for i in data['info']:
        print('Sending email to:',i['email'],i['zipcode'])
        email_content =  html_start +  newsletter_content + betterWeather(i['zipcode']) + word + html_end
        email_content=email_content.replace('</table></div><div class="columns"><table>','')
        email_alert('Daily News - '+todaysDate(),'test',email_content,[i['email']])

if __name__ == "__main__":
    print('Running in Main!')
    email_content =  html_start +  newsletter_content + betterWeather('37122') + word + html_end
    email_content=email_content.replace('</table></div><div class="columns"><table>','')
    email_alert('Daily News - '+todaysDate(),'test',email_content,["bksmith68@gmail.com"])
 
 
