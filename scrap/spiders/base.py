from typing import Dict


class Spider:
    name = None

    @staticmethod
    def pages(url):
        raise NotImplementedError

    @staticmethod
    def parse_page(page_url) -> Dict:
        raise NotImplementedError
