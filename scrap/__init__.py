import settings
from scrap.pipeline import Pipeline


def launch_spider(spider_name):
    spiders_pipeline = Pipeline(spider_name=spider_name, mongo_uri=settings.MONGO_URI)
    spiders_pipeline.process()
