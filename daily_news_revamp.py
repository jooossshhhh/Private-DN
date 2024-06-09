# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:39:25 2023
 
@author: josh.smith
"""
from pprint import pprint
from bs4 import BeautifulSoup
import requests, re, smtplib, datetime, os

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
        # part = MIMEImage(open('C:\\Users\\jpsmi\\fullcoffee.png', 'rb').read())
        # part.add_header('Content-ID', '<image1>')
        # msg.attach(part)
        
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
    # city = "indianapolis"
    # zipcode = '37122'

    geoip = base_url+"/geo/1.0/zip?zip="+zipcode+"&appid="+weather_api
    georesponse = requests.get(geoip)
    x=georesponse.json()
    lat = x['lat']
    lng = x['lon']
    weather_url = base_url + "/data/2.5/weather?lat="+str(lat)+"&lon="+str(lng)+"&appid="+weather_api+"&units=imperial"
    response = requests.get(weather_url)
    y=response.json()
    pprint(y)
    icon_image = "https://openweathermap.org/img/wn/" + y['weather'][0]['icon'] + "@2x.png"
    degree_sign = u'\N{DEGREE SIGN}'
    sunrise = datetime.datetime.fromtimestamp(y['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.datetime.fromtimestamp(y['sys']['sunset']).strftime('%H:%M')
    city = str(y['name'])
    highlow = 'High : ' + str(int(y['main']['temp_max']))+degree_sign + '<br>Low : ' +str(int(y['main']['temp_min']))+degree_sign
    sun = 'Sunrise : ' + str(sunrise) + '<br>Sunset : ' + str(sunset)
    humidity = 'Humidity : ' + str(y['main']['humidity']) + '%'
    # print(y['name'])
    # print(y['main']['temp_max'],'/',y['main']['temp_min'])
    # print(sunrise,sunset)
    # print(y['main']['humidity'],'%')

    """
    weather temp w icon in table format
        weather_template = '<hr><h3>Weather for ' + city + '</h3><br><p ><table><tr><th>' + highlow  + '<br>' + sun + '<br>' + humidity + "</th><th><img src='" + icon_image +"'/></th></tr></table></p>"
    """
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
    print(wotday.getText())
    wotdeff=str(wotdef)
    #print(wotdef)
    
    wotd_def = wotdeff[wotdeff.find('<p>')+3:wotdeff.find('</p>')]
    #print(wotd_def)
    insensitive_wotd = re.compile(re.escape(wotday.getText()), re.IGNORECASE)
    wotd_linked = insensitive_wotd.sub('<a href=https://www.merriam-webster.com/word-of-the-day><em>'+wotday.getText()+'</em></a>', wotd_def)
    # wotd_linked=wotd_def.replace(,'<a href=https://www.merriam-webster.com/word-of-the-day><em>'+wotday.getText()+'</em></a>',1)+''
    print(wotd_linked)
    #return '<div><h3><b>Word of the day</h3>'+wotd_linked+'</div>'
    return '<hr><h3>Word of the Day</h3><br><p>' + wotd_linked +'</p>'
 
word = getWotd()
#print(word)
webscrapeNews()
template = open(r'C:\Users\josh.smith\OneDrive - kennypipe.com\Desktop\DN\email.html')
soup = BeautifulSoup(template.read(), "html.parser")
#word = BeautifulSoup(word, "html.parser")
article_template = soup.find('div', attrs={'class':'columns'})

headline = soup.find('div',attrs={'class':'headline'})
img = headline.img
img['src'] = headline_info[0]['image']
subtitle = headline.p
subtitle.string = headline_info[0]['subtitle'][:300] 
 
link = headline.a
#print(urls[i])
link['href'] = urls[0]
urls.pop(0)
link.string = headline_info[0]['title'][:300]#urls[i]
#print(headline)

#print(headline)
html_start = str(soup)[:str(soup).find(str(article_template))]
#html_start.replace('src=""','src="'+headline_info[0]['image']+'"')

html_end = str(soup)[str(soup).find(str(article_template))+len(str(article_template)):]
 
html_start = html_start.replace('\n','')
html_end = html_end.replace('\n','')
 
#urls=['','','','','','','']
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
    #print(article_template.h1)
    # title = article_template.h1
    # title.string = article['title'][:300]
    #print(article_template.p)
    subtitle = article_template.p
    subtitle.string = article['subtitle'][:300] 
 
    link = article_template.a
    #print(urls[i])
    link['href'] = urls[i]
    link.string = article['title'][:300]#urls[i]
    print(link)
    article_template.a.replace_with(link)
 
    #print(article_template.div['class'])
    newsletter_content += str(article_template).replace('\n','')

#pprint(newsletter_content)
#pprint(newsletter_content)
email_content =  html_start +  newsletter_content + betterWeather('37122') + word + html_end
email_content=email_content.replace('</table></div><div class="columns"><table>','')
#print(email_content)
email_alert('Daily News - '+todaysDate(),'test',email_content,['jp.smith1010@gmail.com'])
 
 
content = """
<!DOCTYPE html>
<html>
<style>
@font-face {
                font-family:valkyrie_c4;
                src:url(data:font/woff;base64,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yaf2JTpqpyODHRnsqJ2OPHbksSOPHbXTUTsdtdORx448dtROR+101E5H7XTUTkftdNROR+101E5H7XTUTkftdNROR+101E5H7XTUTkdeOmqns/JT/O/E/95xzEtH7XTUTkftdNROR+101E5H7XTUTkftdOSlIy8deenIS0deOvLSUTsdtdNROx2101E7HbXTUTsdeemonY7a6aidjtrpqJ2u2uki30W+i3kX8y7mXbXTVTtdtdPFvIt5V+101U5X7XTVTlftdNVOV+101U5X7XTVTlftdNVOV+101U5X7XTVTlftdNVOV+101U5X7XTVTlftdNVOV+105airdrpqp6t2unLUlaOu2umqna7a6aqdrtrpqp2u2umqna7a6cpRV466ctSVo64cdeWoq3a6aqerdrpqp6t2umqnq3a6ctRVO12101U7XbXTVTtdtdNVO12101U7XbXT07n19Cc9nVtP59bTufV0bj2dW0/n1tO59eSoJ0c9nVtP59bTufV0bj2dW0/n1tO59XRuPZ1bT+fW07n1dG49nUlPZ9LTmfR0Jj2dW0/n1tO59XRuPZ1bT+fW07n1OO1x2uO0x2lP59bntM9pn9M+p31O+5z2Oe1z2ue0z2mf0z6nfU77nPY57XPa57TPaZ/TPqd9Tvuc9jntc9rntM9pn9M+p31O+5z2Oe1z2ue0z2mf0z6nfU77nPY5/fXKWui6fr3y63Dm1ysDOqTxPwT+c+U/6W9o7O4Grh+4fuD6gesHrv+N63/j+t+4fuj6oeuHrh+6fuj6ketHrh+5fhxmie+CNgONcajWqD3ap1+EmMeh+uKVXwZ341Br4fpQTVGndEbndEGXQSfuPHHniTtP3HnizhN3nrjzxJ0n7jxx54k7T9x54s4Td56482/DCImao/moITvfrXzuTflz76qfexv93Nvo595GP/c2+rm30c+9jZ6J8My6c2YOPDMHnpn3zsx7Z/7/6sz/X535b6sz/211Ft6L/xr092EEnq38wZV/DF7OwqwVz3zhnn92/KWf/sXxtWui0zPryJk56swcdcb7Ge9nvJ/xfsb7Ge9n1ogza8SZNeLMGnFmjTizRpyZf87MPGdmnjMzz5mZ58zMc47hOYbnGJ5bec+tvOdW23Or7bnKOldZ5yrr3Np3bu07R/7cqnRuPTq3Hp1bj86tR+fWo3Pj//eB2w8r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) format("woff");
                font-style: normal;
}
body{
                max-width:40em;
                margin:0 auto;
                padding:5px;
                font-family:Georgia,serif;
                font-size:20px;
                line-height:30px;
                background-color:#fff;
                color:#000
}
table,
td {
  border-collapse: collapse;
  mso-table-lspace: 0pt;
  mso-table-rspace: 0pt;
 
}
th, td {
  text-align:left;
  padding-bottom: 40px;
  c,olor:#03A062
 
}
h1,h2,h3,dt,small,.small,dl#tweetlist dt,footer,label,#commentlist ol li cite,div.blogparent,input[type="submit"],figcaption{
                font-family:valkyrie_c4;
                font-weight:normal;
                font-style:normal
}
span.url {
                font-family:Georgia,serif;
}
small,.small,footer,dl#tweetlist dt,figcaption{
                font-size:0.8em;
                
}
h1,h2,h3,label{
                line-height:1em
}
h1{
                font-size:2em
}
h2 a{
                color:#000;
                text-decoration: underline
}
h2,h3{
                margin-top:2em
}
h3{
                font-size:1.5em
}
a{
                text-decoration:none;
                color:#20b;
                overflow-wrap:break-word;
                word-wrap:break-word
}
a:visited{
                color:#606
}
a:hover{
                text-decoration:underline
}
dt{
                margin-top:2em;
                font-size:1.2em
}
li,dd{
                margin-bottom:1em
}
figure{
                margin:0
}
blockquote{
                margin:2em;
                color:#444
}
pre{
                overflow-x:auto;
                color:#fff;
                background-color:#333;
                padding:0.25em;
                line-height:1
}
code{
                font-size:0.8em
}
img,iframe,audio{
                max-width:100%;
                display:block
}
img{
                height:auto
}
input[type="text"],input[type="password"],input[type="email"],select,textarea{
                padding:0.5em 0.6em;
                display:block;
                border:1px solid #ccc;
                box-shadow:inset 0 1px 3px #ddd;
                border-radius:4px;
                vertical-align:middle;
                -webkit-box-sizing:border-box;
                -moz-box-sizing:border-box;
                box-sizing:border-box;
                max-width:99%
}
input[type="text"]:focus,input[type="password"]:focus,input[type="email"]:focus,select:focus,textarea:focus{
                outline:0;
                border-color:#129FEA
}
input[type="submit"]{
                padding:5px;
                font-size:1em;
                background:#000;
                color:#fff;
                font-weight:bold
}
form.inlineform input{
                display:inline
}
select{
                height:2.25em;
                border:1px solid #ccc;
                background-color:#fff
}
label{
                margin:0.5em 0 0.2em
}
section{
                margin-bottom:4em
}
section#masthead{
                margin-bottom:1em
}
section#masthead h1{
                margin:0
}
section#masthead h1 a{
                color:#000
}
body#home main h2 small{
                margin-left:2em
}
body#home main ul{
                padding-left:0
}
body#home main ul li{
                list-style-type:none
}
body#home main section#photos img{
                display:inline
}
div.blogparent{
                font-size:1.2em;
                margin:1em 0 -0.5em 0
}
body#oneblog main article header h1{
                margin-bottom:0
}
div#comments ol{
                padding-left:2em
}
div#comments li{
                margin-bottom:2em
}
div#comments li p{
                overflow-wrap:break-word;
                word-wrap:break-word
}
.response{
                display:block;
                margin-left:1em;
                padding:4px;
                background-color:#ffc;
                border:1px solid #000;
                font-family:sans-serif;
                font-size:14px
}
body#book figure img,body#booklist figure img{
                float:left;
                margin-right:2em
}
body#booklist div.abook{
                margin:0 0 8em 0
}
body#interview header h2 a {
                color: #009;
                text-decoration: underline
}
cite {
                color: #666
}
div.presentation_summary{
                margin-bottom:6em
}
@media screen and (max-width: 440px){
                section#masthead h1{
                                font-size:2em
                }
                div.presentation_summary img{
                                display:block
                }
}
@media screen and (min-width: 440px){
                section#masthead h1{
                                font-size:3em
                }
                div.presentation_summary img{
                                float:right
                }
}
@media(prefers-color-scheme:dark){
                body{
                                
                                color:white
                }
                a{
                                color:#88f
                }
                a:visited{
                                color:#aaf
                }
                .response{
                                background-color:#444
                }
                h1,h1 a,h2,h2 a,h3,h3 a,section#masthead h1 a{
                                color:#080
                }
}
ul#reviews {
                margin: 0;
                padding: 0
}
ul#reviews li {
                list-style-type: none
}
ul#reviews li blockquote {
                margin: 1em 0 3em 0
}
ul#reviews li blockquote cite {
                display: block;
                margin-top: 1em
}
#mybooks img { float: left; margin-bottom: 2em; margin-right: 0.5em }
#mybooks h3 { margin-top: 0 }
#mybooks br { clear: both }
 
body#fp dl {
                width: 100%;
                overflow: hidden;
                padding: 0;
                margin: 0
}
body#fp dt {
                font-family:sans; 
                font-size:0.8em; 
                float: left;
                width: 20%;
                padding: 0;
                margin: 0
}
body#fp dd {
                float: left;
                width: 80%;
                padding: 0;
                margin: 0
}
 
</style>
<body id="home">
<section id="masthead">
<h1>first sip.</h1>
</section>
<main>
 
<div>
<table>
<tr>
<h3>Nashville</h3>
High / Low : 86°/65°<br>
Humidity : 52%<br>
Moon Phase : Waning Gibbous<br>
</tr>
<tr>
<h3>Indianapolis</h3>
High / Low : 79°/54°<br>
Humidity : 32%<br>
Moon Phase : Waning Gibbous<br>
</tr>
<h3>News for today</h3>
<table>
<tr>
<th><img alt="Shopping" src=https://www.allsides.com/sites/default/files/styles/200x133/public/e1e4557ffc464b25bf41da282daa8e03-e1682365239646.jpg?itok=ipdT747c width="100%" style="margin: 0; border: 0; padding: 0; display: block;"></th>
<th><a href=https://www.allsides.com/story/politics-rep-george-santos-custody-13-federal-charges style="color: green;background-color: transparent;text-decoration: none;">Rep. George Santos in Custody on 13 Federal Charges</a></th>
</tr>
<tr>
<th><img alt="Shopping" src=https://www.allsides.com/sites/default/files/styles/200x133/public/Screenshot%202023-05-12%20135054.png?itok=QW8aViYa width="100%" style="margin: 0; border: 0; padding: 0; display: block;"></th>
<th><a href=https://www.allsides.com/story/media-industry-tucker-carlson-announces-new-show-twitter-elon-musk-responds style="color: green;background-color: transparent;text-decoration: none;">Tucker Carlson Announces New Show on Twitter; Elon Musk Responds</a></th>
</tr>
<tr>
<th><img alt="Shopping" src=https://www.allsides.com/sites/default/files/styles/feature_image_300x200/public/Biden_40581--13fcd_c0-76-5897-3514_s885x516.jpg?itok=tScPmA1y width="100%" style="margin: 0; border: 0; padding: 0; display: block;"></th>
<th style="text-align:left"><a href=https://www.allsides.com/story/economy-and-jobs-inflation-rose-49-annually-april style="color: green;background-color: transparent;text-decoration: none;">Inflation Rose 4.9% Annually in April</a></th>
</tr>
<tr>
<th><img alt="Shopping" src=https://www.allsides.com/sites/default/files/styles/feature_image_300x200/public/Screenshot%202023-05-11%20171626_0.png?itok=IifB9d4O width="100%" style="margin: 0; border: 0; padding: 0; display: block;"></th>
<th><a href=https://www.allsides.com/story/politics-little-progress-reported-biden-mccarthy-debt-ceiling-meeting style="color: green;background-color: transparent;text-decoration: none;">Little Progress Reported During Biden, McCarthy Debt Ceiling Meeting</a></th>
</tr>
<tr>
<th><img alt="Shopping" src=https://www.allsides.com/sites/default/files/styles/feature_image_300x200/public/CNNtownhall.jpg?itok=6gXoyCii width="100%" style="margin: 0; border: 0; padding: 0; display: block;"></th>
<th><a href=https://www.allsides.com/story/donald-trump-jury-finds-donald-trump-sexually-abused-defamed-e-jean-carroll style="color: green;background-color: transparent;text-decoration: none;">Jury Finds Donald Trump Sexually Abused, Defamed E. Jean Carroll</a></th>
</tr>
</table>
<hr>
An effort made for the happiness of others lifts above ourselves.<br>
-<br>
Lydia M. Child
<hr>
<div style="border-radius:10px; padding: 10px; margin-left: 5px;"><h3><b>Word of the day</h3>
<a href=https://www.merriam-webster.com/word-of-the-day><em>Laden</em></a> describes things that are heavily loaded with something, literally or figuratively.
</div>
<br><br>
<small>Please reply to this email with any suggestions or direct them to jp.smith1010@gmail.com for quicker response time.</small>
</main>   
</body>
</html>
"""
