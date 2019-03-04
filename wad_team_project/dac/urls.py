from django.conf.urls import url
from dac import views

urlpatterns = [
url(r'^$', views.index, name='index'),
]
