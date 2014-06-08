from django.conf.urls import patterns, url, include
from django.contrib import admin
from stock_assign import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stocks/$', 'stock_assign.views.list_stocks', name='stocks'),
    url(r'^orders/$', 'stock_assign.views.list_all_orders', name='orders'),
    url(r'^orders/csv$', 'stock_assign.views.orders_to_csv', name='csv'),
)
