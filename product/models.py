from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category Name")
    slug = models.SlugField(unique=True, verbose_name="Category Slug")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Category")
    name = models.CharField(max_length=255, verbose_name="Product Name")
    slug = models.SlugField(unique=True, verbose_name="Product Slug")  # Ensure it is unique
    description = models.TextField(blank=True, null=True, verbose_name="Product Description")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Product Price")
    quantity = models.IntegerField(verbose_name="Stock")
    available = models.BooleanField(default=True, verbose_name="Available")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    image = models.ImageField(upload_to='uploads/', null=True, blank=True, verbose_name="Product Image")
    thumbnail = models.ImageField(upload_to='uploads/', null=True, blank=True, verbose_name="Product Thumbnail")

    class Meta:
        ordering = ['-date_added']  # Order by date added in descending order

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    @property
    def get_image(self):
        return self.image.url if self.image else '/media/default-image.jpg'
    
    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            self.thumbnail = self.make_thumbnail(self.image)
            self.save()
            return self.thumbnail.url
        return '/media/default-thumbnail.jpg'
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    
    def reduced_image(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(self.image.url))
        return ''
    reduced_image.short_description = 'Image'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
