from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from io import BytesIO
from PIL import Image
from django.core.files import File


class Vendor(models.Model):
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    name = models.CharField(max_length=255)
    # mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)


from django.db import models

# Create your models here.
