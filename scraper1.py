from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape(news_all):
    for news in news_all:
        #News Heading
        try:
            heading = news.find('a').text
        except:
            continue
        
        #Scraping the INDIVIDUAL news article
        news_link = news.find('a')['href']
        
        if news_link in data_frame['Link']:
            continue
        else:
            news_page = requests.get(news_link)
            print("Status code of the article: ", news_page.status_code)
            
            if news_page.status_code == 200:
                soup = BeautifulSoup(news_page.text, 'lxml')
                
                paragraphs = soup.find_all('p')
                
                #Type of the news
                type_para = paragraphs[0].text
                types = type_para[type_para.index(' ')+3: type_para.index(' ',7)]
                
                #Additional Information about the news
                try:
                    more_info = paragraphs[2].text + paragraphs[3].text + paragraphs[4].text + paragraphs[5].text
                except:
                    try:
                        more_info = paragraphs[2].text + paragraphs[3].text + paragraphs[4].text
                    except:
                        more_info = paragraphs[2].text + paragraphs[3].text
                
                #Date of Publication
                try:
                    date = soup.find('span', class_ = 'ok-post-date').text
                except:
                    continue
                
                #Appending to the dictionary
                data_frame['News_Heading'].append(heading)
                data_frame['Date'].append(date)
                data_frame['Type'].append(types)
                data_frame['More_information'].append(more_info)
                data_frame['Link'].append(news_link)
            else:
                continue
        

data_frame = {'News_Heading': [], 'Date': [], 'Type': [], 'More_information': [], 'Link': []}

#SCRAPE onlinekhabar FOR NEWS(ENGLISH)
for page in range(1, 215):
    link = 'https://english.onlinekhabar.com/category/political/page/'+str(page)
    
    html_text1 = requests.get(link)
    print("Status code of page: ", page, ':', html_text1.status_code)
    
    if html_text1.status_code == 200:
        soup = BeautifulSoup(html_text1.text, 'lxml')
        
        news = soup.find_all('div', class_ = 'ok-post-contents')
        scrape(news)
    else:
        continue
    
df = pd.DataFrame(data_frame)

df.to_csv('data_uncleaned_onlinekhabar.csv')