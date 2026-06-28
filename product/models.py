from django.db import models
from django.db.models import Avg, Count


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    @property
    def count(self):
        return self.products.aggregate(count=Count('id'))['count']

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.title
    
    @property
    def rating(self):
        return self.reviews.aggregate(Avg('stars'))['stars__avg']

    
class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    stars = models.IntegerField(choices=((i,i) for i in range(1,6)), null=True)
    def __str__(self):
        return f"Review for {self.product.title}"

