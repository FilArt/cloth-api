# installation
sudo pacman -S python-pipenv
pipenv shell

# launching
gunicorn wsgi:app

# launch spiders
## before launch worker
rq worker

go to "localhost/launch_spider/store_name [adidas|nike]"


# API

## AEP
/items - clothes
/stores - stores

## sorting
/items?sort=baseprice

## pagination
/items?max_results=10&page=5
