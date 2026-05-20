from tkinter import CASCADE
from django.db import models
from django.utils.text import slugify
# Create your models here.

#category model
class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.category_name


#supplier model
class ProductSupplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    supplier_location = models.CharField(max_length=100)

    def __str__(self):
        return self.supplier_name

#product model
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10,decimal_places=2)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='products/',blank=True,null=True)
    product_unit = models.CharField(max_length=5)
    product_slug = models.SlugField(unique=True)
    product_supplier = models.ForeignKey(ProductSupplier,on_delete=models.CASCADE,related_name="products")
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,related_name="products")

    def __str__(self):
        return self.product_name

    def save(self,*args,**kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.product_name)
        super().save(*args,**kwargs)
