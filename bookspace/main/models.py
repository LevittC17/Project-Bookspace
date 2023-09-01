from django.db import models
from main.choices import *


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class BookTag(models.Model):
    name = models.CharField(choices=BookTagChoices.choices, max_length=15)
    description = models.TextField(blank=True, null=True)


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
    thumbnail = models.ImageField(upload_to='book-thumbnails', null=True)


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

# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now_add=True)
#     total_amount = models.DecimalField(max_digits=5, decimal_places=2)
#     is_completed = models.BooleanField(default=False)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     is_rental = models.BooleanField(default=False)
#     rental_due_date = models.DateField(null=True, blank=True)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)


# class Review(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     rating = models.PositiveIntegerField()
#     comment = models.TextField()
