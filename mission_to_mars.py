# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser



def scrape():
    news_list=scrape_news()
    featured_image_url=scrape_images()
    mars_weather=scrape_weather()
    html_table=scrape_facts()
    hemisphere_image_urls=scrape_Hemispheres()

    return({"news":news_list,"image":featured_image_url,"weather":mars_weather,"html":html_table,"hemisphere":hemisphere_image_urls})


def scrape_news():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    response = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('div', class_="slide")


    news_list=[]

    for result in results:
        news_p = result.find('div', class_="rollover_description_inner").text.strip()
        news_title = result.find('img', class_="img-lazy")['alt']    
        news_list.append({"Title":news_title,"Paragraph":news_p})
    
    return (news_list)



def scrape_images():
    #JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    space_image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_image_url)
    browser.click_link_by_partial_text('FULL IMAGE')

    browser.is_element_present_by_text('more info', wait_time=5)
    browser.click_link_by_partial_text('more info')

    image_url=browser.find_link_by_partial_text('.jpg')

    featured_image_url=image_url['href']

    return (featured_image_url)



def scrape_weather():
    #Mars Weather
    weather_url ='https://twitter.com/marswxreport'

    response = requests.get(weather_url, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find('div', class_='js-tweet-text-container')
    mars_weather=results.text.strip()
    
    return(mars_weather)



def scrape_facts():
    # Mars Facts
    facts ='https://space-facts.com/mars/'

    tables = pd.read_html(facts)
    df=tables[0]
    df.columns = ['Fact', 'Value']
    df.set_index('Fact', inplace=True)

    html_table = df.to_html()
    html_table.replace('\n', '')

    return(html_table)

def scrape_Hemispheres():
    # Mars Hemispheres
    Hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    response = requests.get(Hemispheres_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', class_="itemLink product-item")

    url_list=[]

    for x in links:
        url_list.append(f"https://astrogeology.usgs.gov{x['href']}")

    hemisphere_image_urls =[]    
        
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h2')
        links = soup.find('a',text="Sample")
        
        image_urls ={"title": title.text, "img_url": links['href']}
        hemisphere_image_urls.append(image_urls)

    return(hemisphere_image_urls)