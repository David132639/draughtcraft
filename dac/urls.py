from django.conf.urls import url,include
from dac import views
from dac.views import UserRegistrationView


urlpatterns = [
#ajax to support maps and autocomplete
url(r'^api/mapApi/(?P<pub_slug>[\w\-]+)/$',views.map_api,name="map_api"),
url(r'^api/(?P<model_type>[\w\-]+)/$',views.model_api,name="model_api"),

#beers
url(r'^$', views.index, name='index'),
url(r'^beers/$', views.beers, name='beers'),
url(r'^beers/(?P<beer_slug>[\w\-]+)/$', views.beers, name='beers'),
url(r'^beers/(?P<beer_slug>[\w\-]+)/reviews$', views.beers_reviews, name='beer_reviews'),
url(r'^beers/(?P<beer_slug>[\w\-]+)/add_review$', views.add_beer_review, name='beer_add_review'),
url(r'^beers/(?P<beer_slug>[\w\-]+)/stock$', views.update_beer_stock_info, name='beer_update_stock_info'),


#pubs
url(r'^pubs/$', views.pubs, name='pubs'),
url(r'^pubs/(?P<pub_slug>[\w\-]+)/$', views.pubs, name='pubs'),
url(r'^pubs/(?P<pub_slug>[\w\-]+)/beers/$', views.pubs_beers, name='pubs_stocks'),

#generic site stuff
url(r'^search/(?P<query_string>[\w|\W]+)/$',views.search,name='search'),
url(r'^sitemap/$',views.sitemap,name='sitemap'),
url(r'^about/$',views.about,name='about'),
url(r'^privacy/$',views.privacy,name='privacy'),


#accounts, replaced with redux backend, seperate actual logic of app from redux
url(r'^accounts/register/$',UserRegistrationView.as_view(),name='registration_register'),
url(r'^accounts/', include('registration.backends.simple.urls')),

url(r'^accounts/reviews/$', views.user_reviews, name='reviews'),
url(r'^accounts/details/$',views.user_details,name='user_details'),
]
