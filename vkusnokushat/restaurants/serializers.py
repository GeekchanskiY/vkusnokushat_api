from rest_framework import serializers
from .models import Restaurant, RestaurantCountry, RestaurantCategory, RestaurantImage


class RestaurantImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ('id', 'image',)
        read_only_fields = ('id',)


class RestaurantCountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RestaurantCountry
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class RestaurantCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    category = RestaurantCategorySerializer()
    country = RestaurantCountrySerializer()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'work_time', 'place', 'rating', 'description',
                  'main_picture', 'category', 'country')
        read_only_fields = ('id',)

