import requests
from lxml import html
import re
import sys
import dataset

db = dataset.connect('sqlite:///../db/prog.db')
ids = db['albums'].distinct('artist_id')
ids = [id_['artist_id'] for id_ in ids]
artists_table = db['artists']

for artist_id in ids:
    base_url = "http://www.progarchives.com/artist.asp?id={0}"
    url = base_url.format(artist_id)
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit('Non 200 status code received')

    parsed_body = html.fromstring(response.text)

    name = parsed_body.xpath('//div/strong/text()')[0][:-10]
    genre_and_country = parsed_body.xpath('//h2/text()')[0]
    regex_match = re.search(ur'^(.+) \u2022 (.+)$', genre_and_country)
    genre = regex_match.groups()[0]
    country = regex_match.groups()[1]

    artists_table.insert(dict(
        id=artist_id,
        name=name,
        genre=genre,
        country=country
    ))
