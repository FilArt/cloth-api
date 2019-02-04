import asyncio
import time

import json
import logging
from pymongo import MongoClient

from .spiders import (
    AdidasSpider, NikeSpider,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SPIDERS_NUM = 3


class Pipeline:
    def __init__(self, spider_name: str):
        self.mongo_client = MongoClient("mongodb://cloth:cloth@localhost/cloth")
        db = self.mongo_client.cloth
        store_data = db.stores.find_one({"spider_name": spider_name})
        self.store_id = store_data["_id"]
        self.parsing_url = store_data["parsing_url"]
        self.spider = self.get_spider_class(spider_name)()
        self.collection = db.items

    def __del__(self):
        self.mongo_client.close()

    def process(self):
        start = time.time()
        self._process_sync()
        # asyncio.run(self._process())
        end = time.time()
        print(f'elapsed seconds: {end - start:2f}')

    def _process_sync(self):
        for page in self.spider.pages(self.parsing_url):
            self._process_page(page)

    async def _process(self):
        queue = asyncio.Queue()

        queue.put_nowait(self.parsing_url)
        for page in self.spider.pages(self.parsing_url):
            queue.put_nowait(page)

        print('queue_size: {}'.format(queue.qsize()))
        logger.info('queue_size: {}'.format(queue.qsize()))

        tasks = []
        for i in range(queue.qsize()):
            task = asyncio.create_task(self.worker(f'spider-{self.spider.name}-{i}', queue))
            tasks.append(task)

        await queue.join()

        # for task in tasks:
        #     task.cancel()
        await asyncio.gather(*tasks, return_exceptions=False)

        self.mongo_client.close()
        logger.info('process finished')

    async def worker(self, name, queue):
        while True:
            page_url = await queue.get()

            await self._process_page(page_url)

            queue.task_done()

            print(f'spider-{name} processed page {page_url}')

    def process_item(self, item):
        baseprice, salesprice = float(item['baseprice']), float(item['salesprice'])
        images = item['images']
        extra_info = item.get('extra_info')

        assert type(images) in (type([]), type(None))
        assert type(extra_info) in (type({}), type(None))

        # TODO: can i perform this checks during parsing?
        if baseprice < salesprice:
            logger.error(f"for item {item['name']} baseprice = {baseprice}, salesprice = {salesprice}")
            raise Exception("baseprice < salesprice")

        item = {
            'store': self.store_id,
            'name': item['name'],
            'baseprice': baseprice,
            'salesprice': salesprice,
            'url': item['url'],
            'images': images,
            'category': item['category'],
            'sex': item['sex'],
            'extra_info': json.dumps(extra_info),
        }
        self.collection.insert_one(item)

    @staticmethod
    def get_spider_class(spider_name):
        return {
            'adidas': AdidasSpider,
            'nike': NikeSpider,
        }[spider_name]

    def _process_page(self, page_url):
        for item in self.spider.parse_page(page_url):
            self.process_item(item)
        print('finished processing page {page_url}')
