# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

# Import pandas
import pandas as pd

# Import datetime
import datetime as dt

# Import numpy as np 
import numpy as np

def scrape_all():
    # Initiate headless driver for deployent
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "img_urls" : high_def_photo(browser)
    }

    browser.quit()

    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Image Scraping Begins

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and convert dataframe into list of dictionaries 
    df.columns = ['description', 'value']
    mars_description = df['description'].to_list()
    mars_values = df['value'].to_list()
        
    mars_list = []
    for num in np.arange(len(mars_values)):
        row = {'description': mars_description[num], 'value': mars_values[num]}
        mars_list.append(row)

    return mars_list

def high_def_photo(browser):
    # Create list for dictionaries
    img_list = []
    image_search = "Original"
    thumbnail_search = "Sample"
    url = "https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/module_10/Astropedia+Search+Results+_+USGS+Astrogeology+Science+Center.htm"
    browser.visit(url)
    # Hemisphere 1
    tag_1 = "Cerberus Hemisphere Enhanced"
    full_image_elem = browser.find_by_text(f'{tag_1}')
    full_image_elem.click()
    full_image_elem = browser.find_by_text(f'{image_search}')
    url_1 = full_image_elem['href']
    thumbnail_image_elem = browser.find_by_text(f'{thumbnail_search}')
    thumbnail = thumbnail_image_elem['href']
    image_1_dict = {'title': tag_1, 'img_url': url_1, 'thumbnail': thumbnail}
    img_list.append(image_1_dict)
    # Hemisphere 2
    browser.back()
    tag_2 = "Schiaparelli Hemisphere Enhanced"
    full_image_elem = browser.find_by_text(f'{tag_2}')
    full_image_elem.click()
    full_image_elem = browser.find_by_text(f'{image_search}')
    url_2 = full_image_elem['href']
    thumbnail_image_elem = browser.find_by_text(f'{thumbnail_search}')
    thumbnail = thumbnail_image_elem['href']
    image_2_dict = {'title': tag_2, 'img_url': url_2, 'thumbnail': thumbnail}
    img_list.append(image_2_dict)
    # Hemisphere 3
    browser.back()
    tag_3 = "Syrtis Major Hemisphere Enhanced"
    full_image_elem = browser.find_by_text(f'{tag_3}')
    full_image_elem.click()
    full_image_elem = browser.find_by_text(f'{image_search}')
    url_3 = full_image_elem['href']
    thumbnail_image_elem = browser.find_by_text(f'{thumbnail_search}')
    thumbnail = thumbnail_image_elem['href']    
    image_3_dict = {'title': tag_3, 'img_url': url_3, 'thumbnail': thumbnail}
    img_list.append(image_3_dict)
    # Hemisphere 4
    browser.back()
    tag_4 = "Valles Marineris Hemisphere Enhanced"
    full_image_elem = browser.find_by_text(f'{tag_4}')
    full_image_elem.click()
    full_image_elem = browser.find_by_text(f'{image_search}')
    url_4 = full_image_elem['href']
    thumbnail_image_elem = browser.find_by_text(f'{thumbnail_search}')
    thumbnail = thumbnail_image_elem['href']
    image_4_dict = {'title': tag_4, 'img_url': url_4, 'thumbnail': thumbnail}
    img_list.append(image_4_dict)
    
    return img_list

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all()) 
