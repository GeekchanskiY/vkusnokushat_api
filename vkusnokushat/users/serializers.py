from rest_framework import serializers
from .models import TastyUser
from restaurants.models import Restaurant

class RestaurantLikeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'work_time', 'place', 'rating', 'contacts', 'description',
                  'main_picture')
        read_only_fields = ('id',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    likes = RestaurantLikeSerializer(many=True)
    
    class Meta:
        fields = ('id', 'username', 'avatar', 'likes')
        model = TastyUser
        read_only_fields = ('id',)