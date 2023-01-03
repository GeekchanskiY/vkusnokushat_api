from rest_framework import serializers
from .models import TastyUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'username', 'avatar')
        model = TastyUser
        read_only_fields = ('id',)