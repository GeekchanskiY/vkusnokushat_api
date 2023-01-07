from rest_framework import serializers
from .models import Restaurant, RestaurantCountry, RestaurantCategory,\
    RestaurantImage, Review

from users.serializers import UserSerializer


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


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Review
        fields = ('user', 'title', 'text', 'rating')


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    category = RestaurantCategorySerializer()
    country = RestaurantCountrySerializer()
    reviews = ReviewSerializer(source='review_set', many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'work_time', 'place', 'rating', 'contacts', 'description',
                  'main_picture', 'category', 'country', 'reviews')
        read_only_fields = ('id',)
