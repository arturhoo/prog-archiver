import requests
import re
from lxml import html

root_url = 'http://www.progarchives.com/top-prog-albums.asp?syears=2013'
response = requests.get(root_url)
parsed_body = html.fromstring(response.text)
rows = parsed_body.xpath("//table[@cellpadding='7']/tr")

for row in rows:
    tds = row.xpath('.//td')
    rating_str = tds[2].xpath(".//span[contains(@id, 'avgRatings')]/text()")[0]
    rating = float(rating_str)
    qwr_text = tds[2].xpath(".//div[contains(@style, '80%')]/text()")[0]
    qwr = float(re.search(r'(\d.\d+)', qwr_text).groups()[0])
    album = tds[3].xpath(".//strong/text()")[0]
    artist = tds[3].xpath(".//a/text()")[0]
    genre = tds[4].xpath(".//strong/text()")[0]
    year = int(tds[4].xpath("text()")[0][-4:])

    print(artist)
    print('\t' + album)
    print('\t' + str(rating))
    print('\t' + str(qwr))
    print('\t' + genre)
    print('\t' + str(year))
