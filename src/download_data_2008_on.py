import requests
from bs4 import BeautifulSoup
import urllib

url = "http://tsdata.bts.gov/PREZIP/"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')
links_needed = soup.find_all('a')[523:624]
hrefs_needed = [l.attrs['href'] for l in links_needed]

for h in hrefs_needed:
    print "Downloading {}".format(h)
    url = 'http://tsdata.bts.gov' + h
    savepath = './data/2008_on/'
    filename = url.split("Performance_")[1]
    print "Saving as {}".format(filename)
    urllib.urlretrieve(url, savepath + filename)

print "Success!"
