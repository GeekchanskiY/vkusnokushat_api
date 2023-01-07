from django.contrib import admin
from .models import Restaurant, RestaurantCountry, RestaurantCategory, \
    RestaurantImage, Review
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(RestaurantCategory)
admin.site.register(RestaurantCountry)
admin.site.register(RestaurantImage)
admin.site.register(Review)



