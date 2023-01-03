from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class TastyUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='users/', null=True, blank=True)

    # subscribes = models.ManyToManyField("cryptos.Crypto", related_name="sub_cryptos", blank=True)
    # likes = models.ManyToManyField("cryptos.Crypto", related_name="like_cryptos", blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email