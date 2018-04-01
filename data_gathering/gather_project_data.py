import requests
import bs4
import random
import time
import pandas as pd
import csv

###### get the links of the movie
baselink = 'http://www.imdb.com/list/ls057823854/?st_dt=&mode=simple&page='
page = []
for i in list(range(1, 101)):
    page_link = baselink + str(i) + '&ref_=ttls_vw_smp&sort=alpha,asc'
    page.append(page_link)


title_sublink = []
year_list = list(map(str, range(2007, 2018)))
title_sublink_2007to2017 = []
for p in page:
    soup = bs4.BeautifulSoup(requests.get(p).text, 'html5lib')
    main = soup.find('div', attrs={'id': 'main'})
    lister = main.find('div', attrs={'class': 'lister-list'})
    title_span = lister.find_all('span', attrs={'class': 'lister-item-header'})
    # title_image = lister.find_all('div', attrs={'class':'lister-item-image'})

    for s in title_span:
        year = s.find('span', attrs={'class': 'lister-item-year'})
        for y in year_list:
            if y in year.text:
                a = s.a
                href = a['href']
                title_sublink_2007to2017.append(href)

    normal_delay = random.normalvariate(2, 0.5)
    time.sleep(normal_delay)

# save files
#titlelinks = pd.DataFrame(title_sublink_2007to2017)
#titlelinks.to_csv('titlelinks_2007to2017.txt', sep=';', index=None, header=None)




###### get the movie data from IMDB for each movie
with open('titlelinks_2007to2017.txt', 'r') as f:
    reader = csv.reader(f)
    title_sublink_2007to2017 = list(reader)

movie_link = []
for link in title_sublink_2007to2017:
    url = 'http://www.imdb.com' + str(link[0])
    movie_link.append(url)

# movie_link
movie_list = []
movie_link_test = movie_link
for url_m in movie_link_test:
    movie_detial = []
    mtime = None
    color = None
    language = None
    budget = None
    gross = None
    facebook_link = None
    offcialsite = None

    # get the soup of each movie
    msoup = bs4.BeautifulSoup(requests.get(url_m).text, 'html5lib')
    m_main = msoup.find('div', attrs={'id': 'main_top'})
    # get the title of the movie
    title = m_main.find('h1', attrs={'itemprop': 'name'}).text.strip()
    subtext = m_main.find_all('div', attrs={'class': 'subtext'})
    # movie content rating
    if subtext[0].find('meta', attrs={'itemprop': 'contentRating'}):
        moviveclass = subtext[0].find('meta', attrs={'itemprop': 'contentRating'})['content']
    else:
        moviveclass = None
    # movie genre, there are several genre at the same time
    genre_list = subtext[0].find_all('span', attrs={'itemprop': 'genre'})
    genre = [g.text.strip() for g in genre_list]
    # date published
    if subtext[0].find('meta', attrs={'itemprop': 'datePublished'}):
        datepublish = subtext[0].find('meta', attrs={'itemprop': 'datePublished'})['content']
    else:
        datepublish = None
    # get the rating of the movie
    rate = m_main.find('span', attrs={'itemprop': 'ratingValue'}).text.strip()
    # rating count
    ratingCount = m_main.find('span', attrs={'itemprop': 'ratingCount'}).text.strip()
    # get the dirctor(s)
    directorSpan = m_main.find_all('span', attrs={'itemprop': 'director'})
    director = [d.text.strip() for d in directorSpan]
    # get the writer(s)
    writerSpan = m_main.find_all('span', attrs={'itemprop': 'creator'})
    writer = [w.text.strip() for w in writerSpan]
    # get the actors
    actorSpan = m_main.find_all('span', attrs={'itemprop': 'actors'})
    actor = [a.text.strip() for a in actorSpan]
    # get the summary of the movie
    summary = m_main.find('div', attrs={'class': 'summary_text'}).text.strip()

    m_main_bottom = msoup.find('div', attrs={'id': 'main_bottom'})

    # get the description and description writer
    if m_main_bottom.find('div', attrs={'itemprop': 'description'}):
        descriptionDiv = m_main_bottom.find('div', attrs={'itemprop': 'description'})
        description = descriptionDiv.p.text.strip()
        if descriptionDiv.a:
            description_writer = descriptionDiv.a.text.strip()
    else:
        description = None
        description_writer = None

    # plot key words
    if m_main_bottom.find('div', attrs={'itemprop': 'keywords'}):
        plot_keyword_div = m_main_bottom.find('div', attrs={'itemprop': 'keywords'})
        keyword_spanlist = plot_keyword_div.find_all('span', attrs={'itemprop': 'keywords'})
        plot_keyword = [a.text for a in keyword_spanlist]
    else:
        plot_keyword = None

    # including information about country, language, date, filming location, color, budget and aspect ratio, box office
    # and so on.
    content_detail = m_main_bottom.find('div', attrs={'id': 'titleDetails'})
    # time = content_detail.find('time', attrs= {'itemprop':'duration'}).text
    detail = content_detail.find_all('h4', attrs={'class': 'inline'})
    detail_header = [aa.text for aa in detail]
    detail_content = content_detail.find_all('div', attrs={'class': 'txt-block'})
    detail_list = [t.text.strip() for t in detail_content]
    t = detail_list
    # time = [t[i] for i,content in enumerate(t) if content.startswith('Runtime')]
    # color = [t[i] for i,content in enumerate(t) if content.startswith('Color')]
    # language = [t[i] for i,content in enumerate(t) if content.startswith('Language')]
    for content in t:
        if content.startswith('Runtime'):
            mtime = content

        elif content.startswith('Color'):
            color = content

        elif content.startswith('Language'):
            language = content

        elif content.startswith('Budget'):
            budget = content

        elif 'Facebook' in content:
            a = content_detail.div.a
            facebook_link = a['href']

        elif content.startswith('Gross'):
            gross = content

        elif 'Official site' in detail_list:
            offcialsite = 'True'

    if not mtime:
        mtime = None

    if not color:
        color = None

    if not language:
        language = None

    if not budget:
        budget = None

    if not gross:
        gross = None

    if not facebook_link:
        facebook_link = None

    if not offcialsite:
        offcialsite = None

    movie_detial = [title, genre, datepublish, rate, ratingCount, director, writer, actor, summary, description,
                    plot_keyword, mtime, color, language, budget, gross, facebook_link, offcialsite]
    movie_list.append(movie_detial)
    normal_delay = random.normalvariate(1, 0.3)
    time.sleep(normal_delay)

### save imbd data
movie_header = ['Title', 'Genre', 'Datepublish', 'Rate', 'RatingCount', 'Director(s)', 'Writer(s)', 'Actor(s)','Summary', 'Description', 'PlotKeyword', 'Time', 'Color', 'Language', 'Budget', 'Gross','Facebook_link', 'Offcialsite']
df_imdb = pd.DataFrame(movie_list, columns=movie_header)
#df_imdb.to_csv('imbd.txt')
#df_imdb.to_csv('imbd.csv')




###### scrape likes from facebook for each movie
with open('imbd.csv', 'r') as im:
    imbd = pd.DataFrame.from_csv(im, index_col=0, header=0)


movie_with_facebook = imbd.loc[:, ['Title', 'Facebook_link']]
movie_with_facebook = movie_with_facebook.fillna('-')
link_list = movie_with_facebook.values.tolist()


baselink = 'http://www.imdb.com'
# movie_with_link = link_list
for m in link_list:
    if not m[1] == '-':
        movie_link = baselink + m[1]
        m[1] = movie_link


normal_delay = random.normalvariate(2, 0.5)
for movie in link_list:
    like = None
    follow = None
    try:
        if not movie[1] == '-':
            url = movie[1]
            soup = bs4.BeautifulSoup(requests.get(url).text, 'html5lib')
            likes = soup.find_all('div', attrs={'class': 'clearfix _ikh'})
            for i in likes:
                if 'like' in i.text:
                    like = i.text

                if 'follow' in i.text:
                    follow = i.text
    except Exception as e:
        print ('Failed to connect.', movie[0])

    movie.append(like)
    movie.append(follow)
    time.sleep(normal_delay)

df_facebook = pd.DataFrame(link_list)
# save the file
df_facebook.to_csv('facebook_likes.csv')



#########################################################################
###### second part   ###############
###### scrape review ###############

###### scrape review review links for each movie
url = '''http://www.imdb.com/chart/bottom?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=01MRHJ1QF79J1T11TG6N&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_8'''
soup = bs4.BeautifulSoup(requests.get(url).text, 'html5lib')
body = soup.body.tbody
link_list = body.find_all('td', attrs={'class':'titleColumn'})

lowmovie_sublink = []
for title in link_list:
    a = title.a
    href = a['href']
    lowmovie_sublink.append(href)

lowmovie_link =[]
for link in lowmovie_sublink:
    url = 'http://www.imdb.com'+ str(link[:17]) + '?ref_=ttls_li_tt'
    lowmovie_link.append(url)

df = pd.DataFrame(lowmovie_link)
#df.to_csv('lowmovie_link.txt')

review_link =[]
for link in lowmovie_sublink:
    url = 'http://www.imdb.com'+ str(link[:17]) + 'reviews?ref_=tt_urv'
    review_link.append(url)

#review_link
df_reviewlink = pd.DataFrame(review_link)
#df_reviewlink.to_csv('review_link.txt')

###### scrape reviews for each movie by using the review link from above results
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


with open('review_link.txt', 'r') as f:
    reader = csv.reader(f)
    link = list(reader)
    link = link[1:]

# m_url = "http://www.imdb.com/title/tt4458206/reviews?ref_=tt_urv"
# PATIENCE_TIME = 60
# LOAD_MORE_BUTTON_XPATH = '//*[@id="load-more-trigger"]'
review = []
for u in link:
    m_url = u[1]
    driver = webdriver.Chrome('./chromedriver')
    driver.get(m_url)
    normal_delay = random.normalvariate(2, 0.5)

    while True:
        try:
            loadMoreButton = driver.find_element_by_class_name('ipl-load-more__button')
            time.sleep(normal_delay)
            loadMoreButton.click()
            time.sleep(normal_delay)
        except Exception as e:
            print (e)
            break

    print ("Complete")
    time.sleep(normal_delay)
    data_div = driver.find_element_by_id('main')
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(data_html, 'html5lib')
    title = soup.find('h3', attrs={'itemprop': 'name'}).a.text
    lister = soup.find('div', attrs={'class': 'lister-list'})
    review_list = lister.find_all('div', attrs={'class': 'lister-item'})
    for r in review_list:
        if r.find('span', attrs={'class': 'rating-other-user-rating'}):
            rate = r.find('span', attrs={'class': 'rating-other-user-rating'}).text

        review_title = r.find('div', attrs={'class': 'title'}).text.strip()
        content = r.find('div', attrs={'class': 'text'}).text.strip()
        action = r.find('div', attrs={'class': 'actions'}).text.strip()
        review_detail = [title, review_title, rate, content, action]
        review.append(review_detail)

    driver.quit()


df_review = pd.DataFrame(review)
df_review.to_csv('reviews.csv')


