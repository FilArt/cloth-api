import logging
import requests
from lxml import html

from .base import Spider

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

ADIDAS_STORE_URL = 'https://www.adidas.ru'
ADIDAS_OUTLET_STORE_URL = 'https://www.adidas.ru/outlet'

sex_map = {
    # TODO: complete this list and recognise "~" key
    'Женщины': 'f',
    'Мужчины': 'm',
    'Унисекс': 'u',
    'Дети': 'u',
    'Малыши': 'u',
    '~': 'x',
    'Девочки': 'f',
}

HEADERS = {
    'authority': 'www.adidas.ru',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


def strip_adidas(name):
    return name.split(' - ').pop()


class AdidasSpider(Spider):
    name = 'adidas'

    @staticmethod
    def pages(url):
        response = requests.get(url, headers=HEADERS)
        tree = html.fromstring(response.text)
        next_page = tree.cssselect('#top-pagination > ul > li.right-arrow > a')[0].attrib['href']
        if next_page:
            yield url + next_page
            yield from AdidasSpider.pages(next_page)

    @staticmethod
    def parse_page(page_url):
        response = requests.get(page_url, headers=HEADERS)
        tree = html.fromstring(response.text)
        for card in tree.cssselect('div.product-tile'):
            sex_category = card.cssselect('.subtitle')[0].text.split()
            images = card.xpath('.//img')
            carousel_images = [i for i in images if i.attrib.get('data-masterid') is not None]
            if carousel_images:
                while carousel_images:
                    img = carousel_images.pop()
                    baseprice = img.attrib.get('data-basepricevalue')
                    if not baseprice:
                        continue
                    item = {
                        'name': strip_adidas(img.attrib['title']),
                        'baseprice': baseprice.replace(',', ''),
                        'salesprice': img.attrib['data-salespricevalue'],
                        'images': [img.attrib['data-src']],
                        'url': f'{ADIDAS_STORE_URL}{img.attrib["data-url"]}',
                        'category': ' '.join(sex_category[1:]),
                        'sex': sex_map[sex_category[0]],
                        'extra_info': {'master_id': img.attrib['data-masterid']}  # masterid helps with geo
                    }
                    yield item
            else:
                item = {
                    'name': card.cssselect('.title')[0].text,
                    'baseprice': card.cssselect('.baseprice')[0].text.strip().replace('.', ''),
                    'salesprice': card.cssselect('.salesprice')[0].text.strip().replace('.', ''),
                    'images': [card.xpath('.//img/@data-original')[0]],
                    'url': f'{ADIDAS_STORE_URL}{max(card.xpath(".//a/@href"))}',
                    'category': ' '.join(sex_category[1:]),
                    'sex': sex_map[sex_category[0]],
                    'extra_info': {'master_id': card.xpath('.//@data-track')[0]}
                }
                yield item
