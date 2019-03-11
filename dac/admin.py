from django.contrib import admin
from dac.models import UserProfile,Review,Business,Beer,Flavor,Ingredient,User


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Business)
admin.site.register(Beer)
admin.site.register(Flavor)
admin.site.register(Ingredient)