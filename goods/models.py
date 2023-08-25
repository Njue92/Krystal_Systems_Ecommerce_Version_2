from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from shop.models import Vendor


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title

    def get_products(self):
        return Product.objects.filter(sub_category=self)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='img/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='img/', blank=True, null=True)
    location = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10, default=0)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def __str__(self):
        formatted_price = 'Ksh. {:,.2f}'.format(self.price)
        return f'{self.title} - {formatted_price}'


    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return "https://via.placeholder.com/240*180.jpg"

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='img/', blank=True, null=True)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
