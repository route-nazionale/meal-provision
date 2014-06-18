from django.conf.urls import patterns, url, include
from django.contrib import admin
from stock_assign import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stocks/$', 'stock_assign.views.list_stocks', name='stocks'),
    url(r'^vperson/$', 'stock_assign.views.list_vpeople', name='vpeople'),
    url(r'^orders/$', 'stock_assign.views.list_all_orders', name='orders'),
    url(r'^orders/([0-9]*)/([0-9]*)$', 'stock_assign.views.list_orders_from_to', name='orders_from_to'),
    url(r'^orders/filter$', 'stock_assign.views.list_orders_filtered', name='orders_filtered'),
    url(r'^orders/csv$', 'stock_assign.views.all_orders_to_csv_iterator_writer', name='csv'),
    url(r'^orders/csv/([0-9]*)/([0-9]*)$', 'stock_assign.views.orders_to_csv_iterator_writer', name='csv_from_to'),
    url(r'^sums/$', 'stock_assign.views.show_day_counts', name='sums'),
    url(r'^pdf_report/(?P<quartier>[1-5])/(?P<storeroom>[1-5])/((?P<stock>[A-Z])/)?$', 'stock_assign.views.pdf_report', name='pdf_report'),
    
)

