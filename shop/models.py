import secrets

# from PIL import Image
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime, timedelta
# import barcode
# from barcode.writer import ImageWriter
from django.conf import settings
from io import BytesIO
from django.core.files import File
from random import randint


# Create your models here.

class Order(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='Seller', null=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=1,
                               on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', blank=True, null=True, max_length=200, on_delete=models.SET_NULL)
    size = models.PositiveIntegerField(default=0, blank=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    barcode = models.ImageField(upload_to="mediafiles/customer/image/", default='')
    quantity = models.IntegerField(default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        concatenate = '%s -/- %s' % (self.product, self.quantity)
        return concatenate

    # @property
    # def get_cart_total(self):
    #     order_item = self.price
    #     add = sum(order_item)
    #     return add


class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=1,
                               on_delete=models.SET_NULL)
    pr_name = models.CharField(max_length=200, default='')
    price = models.IntegerField(default=0)
    image = models.FileField(upload_to="product/", default='')
    section = models.ForeignKey('Sections', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('category', null=True, on_delete=models.SET_NULL)
    size = models.ManyToManyField('Size', blank=True)
    slug_name = models.SlugField(default='', blank=True)
    stock = models.IntegerField(default=0)
    description = models.TextField(max_length=200, default='')
    code = models.CharField(default='', null=True, blank=True, max_length=9)
    barcode_img = models.ImageField(upload_to="image/", blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    # new_width = models.IntegerField(blank=True, null=True)
    # new_height = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.pr_name)

    def __unicode__(self):
        return self.pr_name

    # def save(self, *args, **kwargs):
    #     EAN = barcode.get_barcode_class('ean13')
    #     secret_key = randint(1000, 2000)
    #     code_num = ('%s%s' % (self.code, secret_key))
    #     ean = EAN(f'{code_num}', writer=ImageWriter())
    #     buffer = BytesIO()
    #     ean.write(buffer)
    #     length = len(str(self.pr_name))
    #     if length <= 0:
    #         conc = '%s %s' % (self.pr_name, self.code[:3])
    #         self.barcode_img.save(f'{conc}_barcode.png', File(buffer), save=False)
    #         return super().save(*args, **kwargs)
    #     else:
    #         conc2 = '%s %s' % (self.pr_name[0:9], self.code[:3])
    #         self.barcode_img.save(f'{conc2}_barcode.png', File(buffer), save=False)
    #         return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

    # def save(self, force_insert=True, force_update=True, using=None, update_fields=None, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         return img.save(self.image.path)


class Category(models.Model):
    catgory = models.CharField(max_length=200, default='', null=False, blank=True)

    def __str__(self):
        return str(self.catgory)


class Review(models.Model):
    product = models.ForeignKey(Product, null=True, related_name="comments", on_delete=models.SET_NULL)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=2, on_delete=models.SET_NULL)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return "%s - %s" % (self.blog, self.name)
        return str(self.product)

    class Meta:
        ordering = ['-date_added']

class Payment(models.Model):
    product = models.ForeignKey('Product', null=True, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return str(f"Payment:{self.amount}")

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        return super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount * 100


Countries = (
    ('Afghanistan', 'Afghanistan'),
    ('Aland Islands', 'Aland Islands'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('American Samoa', 'American Samoa'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Anguilla', 'Anguilla'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas', 'Bahamas'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('British Virgin Islands', 'British Virgin Islands'),
    ('Cambodia', 'Cambodia'),
    ('Nigeria', 'Nigeria'),
    ('Ghana', 'Ghana'),
    ('Egypt', 'Egypt'),
    ('Israel', 'Israel'),
)

PAYMENT_GATEWAYS = (
    ('Credit card', 'Credit card'),
    ('Debit card', 'Debit card'),
    ('PayPal', 'PayPal'),
    ('Stripe', 'Stripe'),
    ('Bitcoin', 'Bitcoin'),
    ('Paystack', 'Paystack'),
)


class CheckOut(models.Model):
    product = models.ForeignKey(Product, default='', on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='seller', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, default='')
    lastname = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=200, default='')
    address = models.CharField(max_length=200, default='')
    address2 = models.CharField(max_length=200, default='', blank=True)
    country = models.CharField(choices=Countries, max_length=100, default='')
    gateway = models.CharField(choices=PAYMENT_GATEWAYS, max_length=100, default='Paypal')
    ordered = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

class Sections(models.Model):
    section_name = models.CharField(max_length=200, default='')
    section_img = models.ImageField(upload_to="mediafiles/sections/", blank=True)

    def __str__(self):
        return str(self.section_name)

class Size(models.Model):
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.value)
