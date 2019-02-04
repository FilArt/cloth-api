# installation
```sh
sudo pacman -S
python-pipenv
pipenv shell
```
# launching
```sh
gunicorn wsgi:app
```
# launch spiders
#### 1) before launch worker
```sh
rq worker
```
#### 2) go to "localhost/launch_spider/store_name [adidas|nike]"

# API

## AEP
##### /items - clothes
##### /stores - stores

## filtering
##### /items?where=baseprice==2690   return all records with baseprice=2690.0
##### /items?where=baseprice<=5000
##### /items/5c559dca0a9ac0096c124b6f  return one item by id

## sorting
##### /items?sort=baseprice

## pagination
##### /items?max_results=10&page=5
