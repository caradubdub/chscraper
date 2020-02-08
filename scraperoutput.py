#libraries here
import re
import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring

def get_image_link(result):
    #GET IMAGE LINK
    # use regex to find start and stop points before the img url and use these to slice out img url

    text = result.text
    start = re.search(r"background-image:url\(", text).end()

    stop = re.search(r"\);\} </style>",text).start()

    image = text[start:stop]
    image480 = re.sub(r"690", r'480', image)
    return image480


def getNames(text):
    namelist = []
    while len(text)>0:
        if (text.count(",")) > 0:
            x = text.find(" by")
            name = (text[:x])
            namelist.append(name)
            y = text.find(", ")
            text = text[y+2:]        
        else: 
            x = text.find("by")
            name = (text[:x])
            namelist.append(name)
            break
    return ', '.join(namelist)

def parse(result,soup,url):
    #GETTING EVENT TITLE
    #~~~~ why is this returning Nonetype
    title = soup.find('h1', class_="ch-page-title__title").get_text()
    #print(title)

    #GETTING DATE AND TIME SEPARATELY
    date = soup.find('span', class_="date").get_text()
    date = date[:-6]
    #print(date)
    time = soup.find('span', class_="time").get_text()
    #print(time)

    #GET LOCATION
    location = soup.find('span', class_="location").get_text()
    #print(location)
        
    #GET PHOTO CAPTION
    caption = (soup.find('div',attrs={"class":"image-wrapper"})["title"])
    #print(caption)

    #GET PHOTO CREDIT
    #returns credit with first and last names of artists
    credit = soup.find('div', class_="ch-page-hero-block__image").get_text()
    #print(credit)
    
    #getting name from credit
    names = getNames(credit)
    out = '<h5 style="text-align: left;">'+date+' at'+time+'<br>'+location+'</h5><h2 style="text-align: left;"><a href='+url+' class="">'+title+'</a></h2>'+caption+credit

    return (out)

def read_url(url):
    result = requests.get(url)

    # check status code to ensure that the website is accessible
    #print(result.status_code)

    #200 code means that website is accessible. 400= not accessible

    #print(result.headers)
    #extract content of the page and store in a variable
    src = result.content

    #pass src variable into B.S module to create B.S object
    soup = BeautifulSoup(src, 'lxml')

    #parse(soup)
    return (result,soup)

#main 
if __name__ == "__main__":
    url=input("enter Carnegie Hall event url:")
    result,soup = read_url(url)
    parse(result,soup,url)
    
    file1 = open("output.txt", "a")
    file1.write(parse(result,soup,url))
    file1.write(get_image_link(result))
    file1.close()
