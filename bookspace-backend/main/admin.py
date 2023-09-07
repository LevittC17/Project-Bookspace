from django.contrib import admin
from main.models import *
# Register your models here.

admin.site.register(Book)
admin.site.register(BookTag)
admin.site.register(Author)
admin.site.register(BookImage)

