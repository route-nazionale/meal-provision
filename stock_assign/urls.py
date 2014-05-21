from django.conf.urls import patterns, url, include
from django.contrib import admin
from stock_assign import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
