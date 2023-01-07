import time

from rest_framework import viewsets
from .serializers import UserSerializer
from .models import TastyUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import FileUploadParser
from django.db.models import Q

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from django.core.exceptions import ObjectDoesNotExist


class UserViewSet(viewsets.ModelViewSet):
    queryset = TastyUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'register':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False, name='register', serializer_class=UserSerializer)
    def register(self, request):
        data = request.data
        try:
            TastyUser.objects.get(username=data["username"])

            return Response({"error": "Такой пользователь уже существует"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        user = TastyUser(
            username=data['username'],
        )
        user.save()
        user.set_password(data["password"])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, name='search', serializer_class=UserSerializer)
    def search(self, request):
        data = request.data.get('search', None)
        if data is not None:
            serializer = UserSerializer(list(self.queryset.filter(Q(username__contains=data))),
                                        many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(list(self.queryset), many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['get', 'options'], detail=False, name='me', serializer_class=UserSerializer)
    def me(self, request):
        data = request.user
        serializer = UserSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, name='change_password', serializer_class=UserSerializer)
    def change_password(self, request):
        data = request.data
        user: TastyUser = request.user
        try:
            user.set_password(data["password"])
        except AttributeError:
            return Response({"detail": "Нет нового пароля!"}, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, name='change_avatar',
            serializer_class=UserSerializer, parser_classes=[FileUploadParser])
    def change_avatar(self, request):
        user = request.user
        try:
            user.avatar = request.FILES['file']
            user.save()
            return Response({"detail": "Аватар успешно обновлён"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.__str__()})


    @action(methods=['post'], detail=False, name='like')
    def like(self, request):
        user = request.user

        data = request.data

        try:
            restaurant = Restaurant.objects.get(name=data.get("name", None))
        except ObjectDoesNotExist:
            return Response({"error": "Такого ресторана не существует"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user.likes.add(restaurant)
            user.save()
            return Response({"message": "Лайк!"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "ошибка"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, name='dislike')
    def dislike(self, request):
        user = request.user

        data = request.data

        try:
            restaurant = Restaurant.objects.get(name=data.get("name", None))
        except ObjectDoesNotExist:
            return Response({"error": "Такого ресторана не существует"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.likes.remove(restaurant)
            user.save()
            return Response({"message": "Дизлайк!"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "ошибка"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, name='dislike')
    def check_like(self, request):
        user = request.user

        data = request.data

        try:
            restaurant = Restaurant.objects.get(name=data.get("name", None))
        except:
            return Response({"error": "Такого ресторана не существует"}, status=status.HTTP_400_BAD_REQUEST)

        if restaurant in user.likes.all():
            return Response({"message": True}, status=status.HTTP_200_OK)
        else:
            return Response({"message": False}, status=status.HTTP_200_OK)


