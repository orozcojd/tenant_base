# tenant-base
Simple web application that display records of items from a sqlite database. Utilizes memcached to serve records if records are already cached. Simple filter feature allows searching through records based off key name.

## 

<div style="max-height:100px; display:flex; justify-content:space-evenly">
  <img src='repo-images/vuejs.png' width="100">
  <img src='repo-images/flask.png' width="100">
  <img src='repo-images/memcached.png' width="100">
  <img src='repo-images/sqlite.png' width="100">
</div>

## Installation
1. Clone Repo
```
$ git clone git@github.com:orozcojd/tenant_base.git
$ cd tenant_base
```
2. Get python3 path (execute following command and use for step 3)
```
$ which python3
```
3. Initialize virtualenv
```
$ pip install virtualenv
$ virtualenv -p /usr/local/bin/python3.8 tbvenv
$ source tbvenv/bin/activate
```
4. Install python-memcache client
```
$ pip install pymemcache
```

## Usage
1. Run the development server
```
$ python main.py
```
2. Navigate to [http://localhost:8000/](http://localhost:8000/)