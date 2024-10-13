from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank= True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name
    
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50) 
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.username
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    shipping_address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.product.name}, Quantity: {self.quantity}"

    def clean(self):
        # Check if the quantity is greater than the stock
        if self.product.stock < self.quantity:
            raise ValidationError(f"Not enough stock for {self.product.name}. Only {self.product.stock} available.")
    
    def save(self, *args, **kwargs):
        # Call the clean method to check stock before saving
        self.clean()

        # Subtract quantity from stock
        self.product.stock -= self.quantity
        self.product.save()

        # Call the parent class save method
        super(Order, self).save(*args, **kwargs)