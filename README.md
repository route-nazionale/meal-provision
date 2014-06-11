Meal Provisioning
=================

This repo contains a Django project with apps to manage
data for meal provision and orders to the caterer.

## Apps

* `stock_assing` : Create a balanced assignement between communities to
be served and stocking points and exports CSV file of the db

## Install and Test

At the moment you can try out the `stock_assign` app.

To do that, clone the repo and navigate to the root folder.

First you need a virtualenv to work in. If you don't have already,
install virtualenvwrapper and create the virtualenv

```
sudo apt-get install virtualenvwrapper
mkvirtualenv rn-django17
```

Now clone the repository, install requirements, create
a settings file and start the development server.

```
git clone git@github.com:route-nazionale/meal_provision.git
cd meal_provision
workon rn-django14
pip install -r requirements.txt
cp meal_provision/settings_dist.py meal_provision/settings.py
# edit meal_provision/settings.py
python manage.py runserver
```

Now point you web browser to http://locahost:8000/stock-assign/

### Test clan assingement algorithm

```
cd stock_assign  
python  
(python) import stock_assigner  
(python) stock_assigner.test()  
```

### Profiling

See the wiki page about Profiling (coming soon)

## Requisiti
* python 2
* django 1.7

other requirements can be found in file `requirements.txt`
