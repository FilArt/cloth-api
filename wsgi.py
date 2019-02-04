import sentry_sdk
from redis import Redis
from rq import Queue
from sentry_sdk.integrations import flask as flask_integration, rq as rq_integration

from app import create_app
from scrap import launch_spider

sentry_sdk.init("https://2576e4b0c73949c1b4e0df0201d7fae3@sentry.io/1385490", integrations=[
    flask_integration.FlaskIntegration(), rq_integration.RqIntegration(),
])

redis_conn = Redis()
q = Queue(connection=redis_conn, default_timeout=10000)

app = create_app()


@app.route("/launch_spider/<string:spider_name>/")
def enqueue_scrapy_job(spider_name):
    if spider_name in [arg for job in q.get_jobs() for arg in job.args]:
        return 'Job already loaded.'
    q.enqueue(launch_spider, spider_name)
    return 'Job successfully loaded.'
