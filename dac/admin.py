from django.contrib import admin
from dac.models import UserProfile,Review,Business,Beer,Flavour,Ingredient

admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Business)
admin.site.register(Beer)
admin.site.register(Flavour)
admin.site.register(Ingredient)