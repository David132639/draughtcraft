from django.conf.urls import url
from dac import views


'''List reviews and pubs subject to change'''

urlpatterns = [

#beers
url(r'^$', views.index, name='index'),
url(r'^beers/$', views.beers, name='beers'),
url(r'^beers/(?P<beer_slug>[\w\-]+)/$', views.beers, name='beers'),
url(r'^beers/(?P<beer_slug>[\w\-]+)/reviews$', views.beers_reviews, name='beers'),
url(r'^beers/(?P<beer_slug>[\w\-]+)/add_review$', views.add_beer_review, name='beers'),


#pubs
url(r'^pubs/$', views.pubs, name='pubs'),
url(r'^pubs/(?P<pub_slug>[\w\-]+)/$', views.pubs, name='pubs'),
url(r'^pubs/(?P<pub_slug>[\w\-]+)/beers/$', views.pubs_beers, name='pubs'),

#user account stuff
url(r'^search/(?P<query_string>[\w\-]+)/$',views.search,name='search'),
url(r'^sitemap/$',views.sitemap,name='sitemap'),

#accounts
url(r'^account/login/$', views.login, name='login'),
url(r'^account/logout/$', views.logout, name='logout'),
url(r'^account/register/$', views.register, name='register'),
url(r'^account/reviews/$', views.user_reviews, name='reviews'),
url(r'^restricted/$', views.restricted, name='restricted'),
]
