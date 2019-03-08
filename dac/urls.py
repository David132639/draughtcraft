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

#generic site stuff
url(r'^search/(?P<query_string>[\w\-]+)/$',views.search,name='search'),
url(r'^sitemap/$',views.sitemap,name='sitemap'),
url(r'^about/$',views.about,name='about'),


#accounts, replaced with redux backend
url(r'^accounts/', include('registration.backends.simple.urls')),
url(r'^accounts/reviews/$', views.user_reviews, name='reviews'),
url(r'^restricted/$', views.restricted, name='restricted'),
]
