from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^drivers', views.drivers, name='drivers'),
    url(r'^routes', views.routes, name='routes'),
    url(r'^blocks', views.blocks, name='blocks'),
    url(r'^tbas', views.tbas, name='tbas'),
]
