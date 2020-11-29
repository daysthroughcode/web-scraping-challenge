# Dependencies
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser():
    # Select Executable Path
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # NASA Mars News 

    # Visit url for NASA Mars News -- Latest News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    #Create Html Object
    news_html = browser.html
    news_soup = bs(news_html, "html.parser")

    # Get article title and paragraph text
    news_article = news_soup.find("div", class_='list_text')
    news_tit = news_soup.find_all('div', class_='content_title')[1].text
    news_para = news_soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL Mars Space Images
    
    jpl_url = "https://www.jpl.nasa.gov"
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    #Create HTML Object
    img_html = browser.html
    img_soup = bs(img_html, "html.parser")

    #Create Featured Image URL
    img_url  = img_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = jpl_url + img_url
    
    # Mars Facts
    
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    #Read Object into pandas
    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    facts_table = mars_df.to_html()
    #mars_df.to_html(facts_table.html)    

    # Mars Hemispheres
    
    #Use Splinter to visit astrogeology website
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    #Create HTML Object
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')

    #set variables and retrieve information for us in loop
    astro_url = 'https://astrogeology.usgs.gov'
    hemi_results = hemi_soup.find('div', class_ = "result-list" )
    hemispheres = hemi_results.find_all('div', class_ = 'item')
    hemisphere_urls = []

    #For loop to iterate through each image
    for hemisphere in hemispheres:
        news_title = hemisphere.find('h3').text
        news_title = news_title.replace("Enhanced", "")
        link_end = hemisphere.find("a")["href"]
        image_link = astro_url + link_end    
        browser.visit(image_link)
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, "html.parser")
        downloads = hemi_soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_urls.append({"title": news_title, "img_url": image_url})
    
    #Store Data In Dictionary
    mars_info = {
        "news_title": news_tit,
        "news_paragraph": news_para,
        "featured_image_url": featured_image_url,
        "mars_facts": facts_table,
        "hemisphere_img_urls": hemisphere_urls
}
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info

if __name__ == '__main__':
    scrape()

