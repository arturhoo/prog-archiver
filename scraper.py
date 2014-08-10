import requests
from lxml import html
import re
import dataset

db = dataset.connect('sqlite:///prog.db')
albums_table = db['albums']

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

    album_id_url = tds[3].xpath(".//a/@href")[0]
    album_id = int(re.search(r'\?id=(\d+)$', album_id_url).groups()[0])
    title = tds[3].xpath(".//strong/text()")[0]
    artist_id_url = tds[3].xpath(".//a/@href")[1]
    artist_id = int(re.search(r'\?id=(\d+)$', artist_id_url).groups()[0])
    artist_name = tds[3].xpath(".//a/text()")[0]

    genre = tds[4].xpath(".//strong/text()")[0]
    year = int(tds[4].xpath("text()")[0][-4:])

    albums_table.insert(dict(
        id=album_id,
        title=title,
        artist_id=artist_id,
        rating=rating,
        qwr=qwr,
        genre=genre,
        year=year
    ))

    print(title)
    print('\t' + str(album_id))
    print('\t' + artist_name)
    print('\t' + str(artist_id))
    print('\t' + str(rating))
    print('\t' + str(qwr))
    print('\t' + genre)
    print('\t' + str(year))
