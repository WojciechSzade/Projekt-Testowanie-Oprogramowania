from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 255, null = False, blank = False)
    description = models.CharField(max_length = 5000, blank=True)
    
    
class Promotion(models.Model):
    name = models.CharField(max_length = 255, null = False, blank = False)
    description = models.CharField(max_length = 5000, blank=True)
    discount = models.FloatField(blank = True, validators=[MinValueValidator(0.0)])
    products = models.ManyToManyField('Product', blank = True, symmetrical=False, related_name='promotions')


class Product(models.Model):
    name = models.CharField(max_length = 255, null = False, blank = False)
    price = models.FloatField(blank = True, validators=[MinValueValidator(0.0)])
    stock = models.IntegerField(blank = True)
    image_url = models.CharField(max_length = 2083, blank = True)
    description = models.CharField(max_length = 5000, blank=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE) # If category is deleted, delete the product
    promotion = models.ForeignKey(Promotion, on_delete = models.SET_NULL, blank = True, null = True) # If promotion is deleted, set promotion to null
    
