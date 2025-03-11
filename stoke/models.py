from django.db import models

# Create your models here.
class Product(models.Model):
    category = models.CharField(max_length=50)
    card_id = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    produced_at = models.CharField(max_length=100)
    expired_on = models.CharField(max_length=100)
    product_number = models.IntegerField()  # Current stock
    sold_number = models.IntegerField(default=0)  # Number of sold products
    last_consumed_at = models.DateTimeField(null=True, blank=True)  # When product was last consumed
    restock_threshold = models.IntegerField(default=10)  # When product needs restocking

    def __str__(self):
        return f'{self.name} and {self.card_id}'
