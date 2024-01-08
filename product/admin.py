from django.contrib import admin
from .models import Category, Product, Material, PopularSolutions

# Register your models here.

admin.site.register(Category)
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(PopularSolutions)

