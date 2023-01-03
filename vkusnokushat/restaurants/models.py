from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class RestaurantCountry(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    work_time = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    rating = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ], default=1)
    description = models.TextField()

    main_picture = models.ImageField(upload_to='restaurants_main/')

    category = models.ForeignKey(RestaurantCategory, on_delete=models.CASCADE)
    country = models.ForeignKey(RestaurantCountry, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_img/', null=True)
