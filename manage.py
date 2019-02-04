import sentry_sdk
from rq import Connection, Worker
from sentry_sdk.integrations.rq import RqIntegration

sentry_sdk.init("https://2576e4b0c73949c1b4e0df0201d7fae3@sentry.io/1385490", integrations=[
    RqIntegration(),
])

with Connection():
    w = Worker('default')
    w.work()
