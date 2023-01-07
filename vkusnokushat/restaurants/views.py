from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from rest_framework import pagination
from django.core.exceptions import ObjectDoesNotExist

from .models import Restaurant, RestaurantImage, RestaurantCountry, RestaurantCategory, Review

from .serializers import RestaurantImageSerializer, RestaurantCategorySerializer, RestaurantCountrySerializer,\
    RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'name'
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == "comment":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(methods=["POST"], name='comment', detail=False)
    def comment(self, request):
        data = request.data
        user = request.user

        restaurant = self.queryset.get(id=data["restaurant"])
        comment = Review(
            user=user,
            restaurant=restaurant,
            rating=data["rating"],
            title=data["title"],
            text=data["text"]
        )
        comment.save()
        return Response({"success": "comment saved!"}, status=status.HTTP_200_OK)


    @action(methods=["POST"], name='search', detail=False)
    def search(self, request):
        # TODO: add django-filter
        data = request.data

        country = data.get("country", None)
        category = data.get("category", None)
        name = data.get("name", None)

        queryset = self.queryset

        if country is not None:
            try:
                country = RestaurantCountry.objects.get(name=country)
            except:
                return Response({"error": "no country"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(country=country)

        if category is not None:
            try:
                category = RestaurantCategory.objects.get(name=category)
            except:
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


        