Meal Provisioning
=================

This repo contains a Django project with apps to manage
data for meal provision and orders to the caterer.

## Apps

* `stock_assing` : Create a balanced assignement between communities to
be served and stocking points

## Install and Test

At the moment you can try out the `stock_assign` app.
This app still is in pre-alpha so no django views are prepared but you can
run a test function written to test the assignement algorithm goodnees.

To do that, clone the repo and navigate to the root folder. Than

`
cd stock_assign
python
>>> import stock_assigner
>>> stock_assigner.test()
`

## Requisiti
* python 2
* django 1.7
