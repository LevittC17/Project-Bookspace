from django.db import models
from main.choices import *


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class BookTag(models.Model):
    name = models.CharField(choices=BookTagChoices.choices, max_length=16)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=60)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, blank=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(BookTag, blank=True)
    publication_date = models.DateField(null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='book-covers')
    thumbnail = models.ImageField(upload_to='book-thumbnails', null=True, editable=False)


class BookInventory(models.Model):
    name = models.OneToOneField(Book, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()

    def add_to_stock_quantity(self):
        self.stock_quantity + 1
        self.save()

    def deduct_stock_quantity(self):
        if self.stock_quantity > 0:
            self.stock_quantity - 1
            self.save()