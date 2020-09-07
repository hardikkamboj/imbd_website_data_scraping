
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv


result = requests.get('https://www.imdb.com/search/title/?title_type=feature,tv_series,documentary&release_date=2000-01-01,2020-09-01&num_votes=50000,&sort=year,desc')

src = result.content
# print(src[:500])
   
soup = BeautifulSoup(src, 'lxml')
html_file = soup.prettify()[:10000]
# print(len(html_file))

names = []
years = []
ratings = []
list_votes = []
genres = []
directors = []
actors = []
list_information = []


for link in soup.find_all('div',class_ = 'lister-item mode-advanced'):
	name = link.h3.a.text
	year = link.h3.find('span',class_ = "lister-item-year text-muted unbold").text
	rating = link.find('strong').text
	votes = link.find('span',attrs = {'name':'nv'}).text
	genre = link.find('span',class_ = 'genre').text
	genre = " ".join(genre.split())
	director= link.find('p',class_='').find_all('a')[0].text

	actor = [a.text for a in link.find('p',class_='').find_all('a')[1:]]

	information = link.find_all('p',class_ = 'text-muted')[1].text
	information = " ".join(information.split())

	
	names.append(name)
	years.append(year)
	ratings.append(rating)
	list_votes.append(votes)
	genres.append(genre)
	directors.append(director)
	actors.append(actor)
	list_information.append(information)


# with open('index', 'w') as f:
#     for item in temp:
#         f.write("%s\n" % item)print(type(temp))

df = pd.DataFrame({'Name':names,'Year':years,'Ratings':ratings,'Votes':list_votes,
					'Genres':genres,'Directors':directors,'Actors':actors,
					'Information':list_information})
print(df.head())
df.to_csv('data.csv')
