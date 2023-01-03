from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from rest_framework import pagination
from django.core.exceptions import ObjectDoesNotExist

from .models import Restaurant, RestaurantImage, RestaurantCountry, RestaurantCategory

from .serializers import RestaurantImageSerializer, RestaurantCategorySerializer, RestaurantCountrySerializer,\
    RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'name'
    permission_classes = [permissions.AllowAny]

    @action(methods=["POST"], name='search', detail=False)
    def search(self, request):
        # TODO: add django-filter
        data = request.data

        country = data.get("country", None)
        category = data.get("category", None)
        name = data.get("name", None)

        queryset = self.queryset

        if country is not None:
            country = RestaurantCountry.objects.filter(name=country)
            if len(country) == 0:
                return Response({"error": "no country"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(country=country)

        if category is not None:
            category = RestaurantCategory.objects.filter(name=category)
            if len(category) == 0:
                return Response({"error": "no category"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(category=category)

        if name is not None:
            queryset = queryset.filter(name__contains=name)

        return Response(self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK)


class RestaurantImageViewSet(viewsets.ModelViewSet):
    queryset = RestaurantImage.objects.all()
    serializer_class = RestaurantImageSerializer
    lookup_field = 'restaurant'
    permission_classes = [permissions.AllowAny]


        