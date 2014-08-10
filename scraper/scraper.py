import requests
from lxml import html
import re
import dataset
import sys

db = dataset.connect('sqlite:///../db/prog.db')
albums_table = db['albums']

for year in range(1945, 2015):
    base_url = "http://www.progarchives.com/top-prog-albums.asp?syears={0}"
    url = base_url.format(year)
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit('Non 200 status code received')

    parsed_body = html.fromstring(response.text)
    rows = parsed_body.xpath("//table[@cellpadding='7']/tr")

    for row in rows:
        tds = row.xpath('.//td')

        rating_str = tds[2].xpath(".//span[contains(@id, 'avgRatings')]/text()")[0]
        rating = float(rating_str)
        qwr_text = tds[2].xpath(".//div[contains(@style, '80%')]/text()")[0]
        qwr = float(re.search(r'(\d.\d+)', qwr_text).groups()[0])
        ratings = int(tds[2].xpath(".//span[contains(@style, '100%')]/text()")[0])

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
            ratings=ratings,
            genre=genre,
            year=year
        ))
