from bs4 import BeautifulSoup
import pandas as pd
import requests

news_dictionary = {'title': [], 'text': [], 'date': [], 'Link': []}

for page in range(100,200):
    main_page = requests.get('https://www.cbsnews.com/latest/world/'+str(page)+'/')
    print('Status code of the page:', page, ': ' ,main_page.status_code)
    if main_page.status_code == 200:
        soup_main = BeautifulSoup(main_page.text, 'lxml')
        news_articles = soup_main.find_all('a', class_ = 'item__anchor')
        for news in news_articles:
            try:
                link = news['href']
            except:
                continue
            if link in news_dictionary['Link']:
                continue
            else:
                news_page = requests.get(link)
                print('Status code of the news page: ', news_page.status_code)
                if news_page.status_code == 200:
                    soup_news = BeautifulSoup(news_page.text, 'lxml')
                    try:
                        header = soup_news.find('div', class_ = 'content__high-wrapper')
                        heading = header.find('h1').text
                        date = header.find('time').text
                    except:
                        continue
                    try:
                        content = soup_news.find('section', class_ = 'content__body')
                        paragraphs = content.find_all('p')
                        try:
                            text = paragraphs[0].text + paragraphs[1].text + paragraphs[2].text + paragraphs[3]
                        except:
                            try:
                                text = paragraphs[0].text + paragraphs[1].text + paragraphs[2].text
                            except:
                                try:
                                    text = paragraphs[0].text + paragraphs[1].text
                                except:
                                    try:
                                        text = paragraphs[0].text
                                    except:
                                        continue
                    except:
                        continue
                    news_dictionary['date'].append(date)
                    news_dictionary['Link'].append(link)
                    news_dictionary['title'].append(heading)
                    news_dictionary['text'].append(text)
                else:
                    continue
    else:
        continue

df2 = pd.DataFrame(news_dictionary)