from django.db import models

# Create your models here.
class Product(models.Model):
    category = models.CharField(max_length=50)
    card_id = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    produced_at = models.CharField(max_length=100)
    expired_on = models.CharField(max_length=100)
    product_number = models.IntegerField()

    def __str__(self):
        return self.name