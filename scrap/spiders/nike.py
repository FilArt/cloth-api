import json
import logging
import requests
from urllib.parse import urlparse

from .base import Spider

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def get_sex(item_description):
    if 'Женск' in item_description:
        return 'f'
    elif 'Мужск' in item_description:
        return 'm'
    else:
        return 'u'


class NikeSpider(Spider):
    name = 'nike'

    @staticmethod
    def pages(url):
        response = requests.get(url)
        next_page = response.json().get('nextPageDataService')
        if next_page:
            next_page = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url)) + next_page
            yield next_page
            yield from NikeSpider.pages(next_page)

    @staticmethod
    def parse_page(page_url):
        response = requests.get(page_url)
        data = json.loads(response.text)
        items = data['sections'][0]['items']
        items = list(filter((lambda i: not i['inWallContentCard']), items))

        for item in items:
            yield {
                'name': item['title'],
                'baseprice': item['overriddenLocalPrice'].replace(' pyб.', '').replace(' ', ''),
                'salesprice': item['rawPrice'],
                'images': [item['spriteSheet']],
                'url': item['pdpUrl'],
                'category': item['subtitle'],
                'sex': get_sex(item['subtitle']),
            }
