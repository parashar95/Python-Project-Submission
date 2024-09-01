from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
# Configure Selenium to use Chrome
options = Options()
options.headless = True  # Run in headless mode (no browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://www.imdb.com/chart/top/'
driver.get(url)
html = driver.page_source

def get_soup(url):
    driver.get(url)
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')


soup = get_soup(url)

ulTags = soup.find_all('ul')

url_list = []

for ulTag in ulTags:
    if ulTag.has_attr('class'):
        class_list = ulTag['class']
        if 'ipc-metadata-list' in class_list and 'compact-list-view' in class_list:
            # find the a tag with class name 'ipc-title-link-wrapper'
            aTags = ulTag.find_all('a')
            for aTag in aTags:
                if aTag.has_attr('class'):
                    class_list = aTag['class']
                    if 'ipc-title-link-wrapper' in class_list:
                        url_list.append(aTag['href'])

# print(url_list)
movies = []

max = 10

isAll = True

i = 0

for url in url_list:
    this_movie = {}
    soup = get_soup(f'https://www.imdb.com{url}')
    # find the span tag with class name 'hero__primary-text'
    spanTag = soup.find('span', class_='hero__primary-text')

    if spanTag:
        this_movie['title'] = spanTag.text

    genreDiv = soup.find('div', class_='ipc-chip-list__scroller')

    genres = ''
    if genreDiv:
        genreTags = genreDiv.find_all('a')
        for genreTag in genreTags:
            genres += genreTag.text + ', '

    this_movie['genres'] = genres
            
    # data-testid="hero-rating-bar__aggregate-rating__score"
    ratingDiv = soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating'})
    if ratingDiv:
        ratingSpan = ratingDiv.find('span')
        if ratingSpan:
            print("ratingSpan::", ratingSpan.text)
            this_movie['rating'] = ratingSpan.text.split('/')[0]

    data = []
    all_uls = soup.find_all('ul')
    for ul in all_uls:
        if ul.has_attr('class'):
            class_list = ul['class']
            # ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt
            if 'ipc-inline-list' in class_list and 'ipc-inline-list--show-dividers' in class_list:
                liTags = ul.find_all('li')
                for liTag in liTags:
                    data.append(liTag.text)
    this_movie['year'] = data[4]
    movies.append(this_movie)
    i += 1

    if i == max and not isAll:
        break

print(movies)


# Create a DataFrame from the movies list
df = pd.DataFrame(movies)

# Save the DataFrame to an Excel file
df.to_excel('movies.xlsx', index=False)


