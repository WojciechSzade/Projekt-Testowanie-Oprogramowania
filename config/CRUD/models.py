from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 255, null = False, blank = False)
    price = models.FloatField(blank = True, validators=[MinValueValidator(0.0)])
    stock = models.IntegerField(blank = True)
    image_url = models.CharField(max_length = 2083, blank = True)
    description = models.CharField(max_length = 5000, blank=True)