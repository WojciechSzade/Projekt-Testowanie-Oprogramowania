from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError

# Create your models here.
class Category(models.Model):
    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            raise ValidationError('Name cannot be empty or none')
        super(Category, self).save(*args, **kwargs)
        
    name = models.CharField(max_length = 255, null = False, blank = False)
    description = models.CharField(max_length = 5000, blank=True, null = True)
    
    
class Promotion(models.Model):
    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            raise ValidationError('Name cannot be empty or none')
        if self.discount is None:
            raise ValidationError('Discount cannot be none')
        if self.discount < 0:
            raise ValidationError('Discount cannot be negative')
        super(Promotion, self).save(*args, **kwargs)
        
    name = models.CharField(max_length = 255, null = False, blank = False)
    description = models.CharField(max_length = 5000, blank=True, null = True)
    discount = models.FloatField(blank = True, null = True, validators=[MinValueValidator(0.0)])
    products = models.ManyToManyField('Product', blank = True, symmetrical=False, related_name='promotions')


class Product(models.Model):
    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            raise ValidationError('Name cannot be empty or none')
        if self.category is None:
            raise ValidationError('Category cannot be none')
        if self.price is None:
            raise ValidationError('Price cannot be none')
        if self.stock is None:
            raise ValidationError('Stock cannot be none')
        if self.price < 0:
            raise ValidationError('Price cannot be negative')
        super(Product, self).save(*args, **kwargs)
    
    name = models.CharField(max_length = 255, null = False, blank = False)
    price = models.FloatField(blank = False, null = False, validators=[MinValueValidator(0.0)])
    stock = models.IntegerField(blank = False, null = False)
    image_url = models.CharField(max_length = 2083, blank = True, null = True)
    description = models.CharField(max_length = 5000, blank=True, null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE) # If category is deleted, delete the product
    promotion = models.ForeignKey(Promotion, on_delete = models.SET_NULL, blank = True, null = True) # If promotion is deleted, set promotion to null
    
