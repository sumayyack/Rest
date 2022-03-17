from django.db import models

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=120)
    product_image=models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name


class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    purchase_price=models.PositiveIntegerField()
    selling_price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()