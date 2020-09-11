
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randint
import time
from IPython.core.display import clear_output


list_url = ['https://www.imdb.com/search/title/?title_type=feature,tv_series,documentary&release_date=2000-01-01,2020-09-01&num_votes=50000,&sort=year,desc']
temp = 'https://www.imdb.com/search/title/?title_type=feature,tv_series,documentary&release_date=2000-01-01,2020-09-01&num_votes=50000,&sort=year,desc&start='
temp_2 = '&ref_=adv_nxt'
remaining_urls = [temp + str(i) + temp_2 for i in range(51,2500,50)]
list_url.extend(remaining_urls)

total_requests = 0

# print(len(html_file))

names = []
years = []
ratings = []
list_votes = []
genres = []
directors_stars = []
actors = []
list_information = []

program_starts = time.time()

for url in list_url:		
	result = requests.get(url)
	sleep(randint(8,15))
	src = result.content
	# print(src[:500])

	total_requests += 1
	elapsed_time = time.time() - program_starts
	print('Request:{}; Frequency: {} requests/s'.format(total_requests, total_requests/elapsed_time))
	clear_output(wait = True)
   
	soup = BeautifulSoup(src, 'lxml')
	html_file = soup.prettify()[:10000]
	for link in soup.find_all('div',class_ = 'lister-item mode-advanced'):
		name = link.h3.a.text
		year = link.h3.find('span',class_ = "lister-item-year text-muted unbold").text
		rating = link.find('strong').text
		votes = link.find('span',attrs = {'name':'nv'}).text
		genre = link.find('span',class_ = 'genre').text
		genre = " ".join(genre.split())

		dir_star = [a.text for a in link.find('p',class_='').find_all('a')[:]]

		information = link.find_all('p',class_ = 'text-muted')[1].text
		information = " ".join(information.split())

		
		names.append(name)
		years.append(year)
		ratings.append(rating)
		list_votes.append(votes)
		genres.append(genre)
		directors_stars.append(dir_star)
		list_information.append(information)


# with open('index', 'w') as f:
#     for item in temp:
#         f.write("%s\n" % item)print(type(temp))

df = pd.DataFrame({'Name':names,'Year':years,'Ratings':ratings,'Votes':list_votes,
					'Genres':genres,'Directors_stars':directors_stars,
					'Information':list_information})
print(df.head())
df.to_csv('data.csv')
