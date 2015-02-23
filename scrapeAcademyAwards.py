from bs4 import BeautifulSoup
from urllib2 import urlopen
import mechanize
import json

BASE_URL = 'http://awardsdatabase.oscars.org/ampas_awards/BasicSearchInput.jsp'
browser = mechanize.Browser()

years = []
movies = []

awardDict = {}

browser.open(BASE_URL)
browser.select_form(name='basicSearchInput')
browser['BSFromYear'] = ['1']
browser['BSToYear'] = ['86']
browser['BSCategory'] = ['1081']
browser.find_control('BSWinner').items[0].selected = True
browser.submit()

soup = BeautifulSoup(browser.response().read())

for year in soup.find_all('a', {'class': 'awardYearHeader'}):
	years.append(year.contents[0][:4])

for movie in soup.find_all('div', {'class': 'nomHangIndent'}):
	movies.append(movie.find('a').contents[0])

for i in xrange(0,len(years)):
	awardDict[years[i]] = movies[i]
	pass

with open('AcademyAwards.json', 'w') as outfile:
	jsonData = json.dumps(awardDict, outfile, sort_keys=True, indent=4, ensure_ascii=False)
	outfile.write(jsonData)
	outfile.close()