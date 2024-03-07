from django.db import models
from authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return f'Category({self.name}->{self.id})'

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    AVAILABILITY = (
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('AVAILABLE', 'Available'),
        ('COMING_SOON', 'Coming Soon'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    price = models.FloatField()
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, related_name="products"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True
    )
    image = models.ImageField(upload_to='media/products')
    availability = models.CharField(
        max_length=20, 
        choices=AVAILABILITY, 
        default='Available'
    )
    prod_count = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'Product({self.id})'

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=5000)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        db_table = 'review'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'