from django.contrib import admin

from .models import Category, Genre, Title, Review


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
