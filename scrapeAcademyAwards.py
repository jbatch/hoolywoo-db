from bs4 import BeautifulSoup
import mechanize
import json
import requests

AADB_URL = 'http://awardsdatabase.oscars.org/ampas_awards/BasicSearchInput.jsp'
AA_WIKI_URL = 'http://en.wikipedia.org/wiki/List_of_Academy_Awards_ceremonies'
browser = mechanize.Browser()

years = []
movies = []
awardDates = []
releaseDates = []

awardDict = {}

soup = BeautifulSoup(requests.get(AA_WIKI_URL).text)

for row in soup('table')[1].findAll('tr')[3:]:
	tds = row.findAll('td')
	if(len(tds) > 1):
		awardDates.append(tds[1].contents[0])

browser.open(AADB_URL)
browser.select_form(name='basicSearchInput')
browser['BSFromYear'] = ['3']
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
	url = "http://www.omdbapi.com/?t=" + movies[i].replace(' ', '+') + '&y=&plot=short&r=json'
	released = json.loads(requests.get(url).text)['Released']
	awardDict[years[i]] = {'Movie': movies[i], 'AwardDate': awardDates[i], "ReleaseDate": released}
	pass

with open('AcademyAwards.json', 'w') as outfile:
	jsonData = json.dumps(awardDict, outfile, sort_keys=True, indent=4, ensure_ascii=False)
	outfile.write(jsonData)
	outfile.close()
