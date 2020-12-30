from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    pecent_of_discount = models.IntegerField(default=1, validators=[
        MaxValueValidator(99),
        MinValueValidator(1)
    ])
    user = models.ManyToManyField(
        User, through='Client_Discount', through_fields=('discount', 'user'))

    def __str__(self):
        return self.name


class Client_Discount(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
